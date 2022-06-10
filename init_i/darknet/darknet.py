import cv2, os, shutil, time, sys, copy, logging
import numpy as np
import tensorrt as trt

sys.path.append(f'{os.getcwd()}')
from init_i.utils.logger import config_logger
from init_i.utils.timer import Timer
from init_i.common import common
from init_i.common.common import Model
from init_i.utils.parser import load_json, load_txt, parse_config
import ctypes

class Darknet(Model):

    def __init__(self, idx):
        logging.info('Load darknet libarary ...')
        try:
            ctypes.cdll.LoadLibrary('./plugins/libyolo_layer.so')
            logging.info('Load libarary success !!! (./plugins/libyolo_layer.so)')
        except OSError as e:
            raise Exception('Failed to load ./plugins/libyolo_layer.so.  '
                             'Did you forget to do a "make" in the "./plugins/" '
                             'subdirectory?')
        super(Darknet, self).__init__(idx)


    def load_model(self, conf):
        
        conf = parse_config(conf)

        # parse information from configuration and get palette.
        (   self.input_size, self.out_size, self.preprocess, 
            self.thres, self.dynamic_shape ) = self.parse_param(conf)
        
        # init engine
        engine_path = conf['model_path']
        max_batch_size = -1 if self.dynamic_shape !=None else 1
        ([context, inputs, outputs, bindings, stream]) = self.init_engine(engine_path, max_batch_size)
        
        # clear context
        self.clear_runtime()

        # return trt_objects and palette
        palette = self.get_palette(conf)
        return ( [context, inputs, outputs, bindings, stream], palette)
    
    def norm(self, data):
        return ((data - np.min(data)) / (np.max(data) - np.min(data)))

    def custom_norm(self, data):
        old_min = np.min(data)
        old_max = np.max(data)
        old_range = old_max - old_min
        new_min = 0
        new_max = 1
        new_range = new_max - new_min
        return ( (data-old_min)*(new_range/old_range) + new_min )

    def softmax(self, x):

        y = np.exp(x - np.max(x))
        f_x = y / np.sum(np.exp(x))
        return f_x

    def softmax2d(self, x):
        
        max = np.max(x,axis=1,keepdims=True) #returns max of each row and keeps same dims
        e_x = np.exp(x - max) #subtracts each row with its max value
        sum = np.sum(e_x,axis=1,keepdims=True) #returns sum of each row and keeps same dims
        f_x = e_x / sum 
        return f_x

    """ Do Inference """
    def inference(self, trt_objects, frame, conf):
        
        conf = parse_config(conf)

        out_resolution = conf["output_resolution"] if 'output_resolution' in conf.keys() else None
        labels = load_txt(conf['label_path'])
        input_shape = tuple(map(int, conf['input_size'].strip('()').split(',')[1:]))
        thres = float(conf['thres'])
        nms_thres = float(conf['nms_thres'])
        
        # tidy up the return information 
        info = {
            "frame": None,                          # placeholder for frame.
            "output_resolution": out_resolution,    # the resize proportion output resolution.
            "detections": []                              # each object's information ( { xmin, ymin, xmax, ymax, label, score, id } ).
        }

        temp_dets = {                      
            "xmin": None,                         # In classification, we will draw the result on the fixed position.
            "ymin": None,
            "xmax": None,
            "ymax": None,
            "label": None,                      # the placeholder for label.
            "score": None,                      # the placeholder for probability.
            "id": None,                         # the placeholder for the indext with the maxmium value.
        }

        # parsing tensorrt objects
        [ context, inputs, outputs, bindings, stream ] = trt_objects    
        
        # For web api and multi
        self.store_runtime()

        # pre-process
        # pre_frame = preproc(image=frame.copy(), size=self.input_size[-2:], mode=self.preprocess) 
        pre_frame = _preprocess_yolo(frame.copy(), input_shape)
        np.copyto(inputs[0].host, pre_frame.ravel())    # copy buffer into device

        # do inference.
        t_infer = Timer()
        results= common.do_inference(context, bindings=bindings, inputs=inputs, outputs=outputs, stream=stream, dynamic_shape=self.dynamic_shape)
        
        # update frame into info['frame']
        info['frame']=frame.copy()

        # map each result into detections
        if results:
            # NEW ..............................
            boxes, scores, classes = _postprocess_yolo(
                results, frame.shape[1], frame.shape[0], thres,
                nms_threshold=0.5, input_shape=input_shape,
                letter_box=False)

            for idx in range(len(scores)):

                # parse the result after classification
                x1, y1, x2, y2 = boxes[idx]
                
                # new_temp_dets = temp_dets.copy()
                new_temp_dets = copy.deepcopy(temp_dets)
                new_temp_dets['xmin'] = x1
                new_temp_dets['xmax'] = x2
                new_temp_dets['ymin'] = y1
                new_temp_dets['ymax'] = y2
                new_temp_dets['id'] = int(classes[idx])
                new_temp_dets['label'] = labels[new_temp_dets['id']]
                new_temp_dets['score'] = float(scores[idx])

                info['detections'].append(new_temp_dets)           

        self.clear_runtime()
        return info

    """ Parse parameters from config """
    def parse_param(self, conf):

        conf = parse_config(conf)
        input_size = tuple(map(int, conf['input_size'].split(","))) # c, h, w
        out_size = [ input_size[1]//4, input_size[2]//4 ]
        preprocess = conf['preprocess']
        thres = float(conf['thres'])
        dynamic_shape = (1,)+input_size if 'dynamic_batch' in conf.keys() else None # setup with one batch -> ( 1, 3, h, w)

        return input_size, out_size, preprocess, thres, dynamic_shape


def _preprocess_yolo(img, input_shape, letter_box=False):
    """Preprocess an image before TRT YOLO inferencing.

    # Args
        img: int8 numpy array of shape (img_h, img_w, 3)
        input_shape: a tuple of (H, W)
        letter_box: boolean, specifies whether to keep aspect ratio and
                    create a "letterboxed" image for inference

    # Returns
        preprocessed img: float32 numpy array of shape (3, H, W)
    """
    if letter_box:
        img_h, img_w, _ = img.shape
        new_h, new_w = input_shape[0], input_shape[1]
        offset_h, offset_w = 0, 0
        if (new_w / img_w) <= (new_h / img_h):
            new_h = int(img_h * new_w / img_w)
            offset_h = (input_shape[0] - new_h) // 2
        else:
            new_w = int(img_w * new_h / img_h)
            offset_w = (input_shape[1] - new_w) // 2
        resized = cv2.resize(img, (new_w, new_h))
        img = np.full((input_shape[0], input_shape[1], 3), 127, dtype=np.uint8)
        img[offset_h:(offset_h + new_h), offset_w:(offset_w + new_w), :] = resized
    else:
        img = cv2.resize(img, (input_shape[1], input_shape[0]))

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.transpose((2, 0, 1)).astype(np.float32)
    img /= 255.0
    return img


def _nms_boxes(detections, nms_threshold):
    """Apply the Non-Maximum Suppression (NMS) algorithm on the bounding
    boxes with their confidence scores and return an array with the
    indexes of the bounding boxes we want to keep.

    # Args
        detections: Nx7 numpy arrays of
                    [[x, y, w, h, box_confidence, class_id, class_prob],
                     ......]
    """
    x_coord = detections[:, 0]
    y_coord = detections[:, 1]
    width = detections[:, 2]
    height = detections[:, 3]
    box_confidences = detections[:, 4] * detections[:, 6]

    areas = width * height
    ordered = box_confidences.argsort()[::-1]

    keep = list()
    while ordered.size > 0:
        # Index of the current element:
        i = ordered[0]
        keep.append(i)
        xx1 = np.maximum(x_coord[i], x_coord[ordered[1:]])
        yy1 = np.maximum(y_coord[i], y_coord[ordered[1:]])
        xx2 = np.minimum(x_coord[i] + width[i], x_coord[ordered[1:]] + width[ordered[1:]])
        yy2 = np.minimum(y_coord[i] + height[i], y_coord[ordered[1:]] + height[ordered[1:]])

        width1 = np.maximum(0.0, xx2 - xx1 + 1)
        height1 = np.maximum(0.0, yy2 - yy1 + 1)
        intersection = width1 * height1
        union = (areas[i] + areas[ordered[1:]] - intersection)
        iou = intersection / union
        indexes = np.where(iou <= nms_threshold)[0]
        ordered = ordered[indexes + 1]

    keep = np.array(keep)
    return keep


def _postprocess_yolo(trt_outputs, img_w, img_h, conf_th, nms_threshold,
                      input_shape, letter_box=False):
    """Postprocess TensorRT outputs.

    # Args
        trt_outputs: a list of 2 or 3 tensors, where each tensor
                    contains a multiple of 7 float32 numbers in
                    the order of [x, y, w, h, box_confidence, class_id, class_prob]
        conf_th: confidence threshold
        letter_box: boolean, referring to _preprocess_yolo()

    # Returns
        boxes, scores, classes (after NMS)
    """
    # filter low-conf detections and concatenate results of all yolo layers
    detections = []
    for o in trt_outputs:
        detections = o.reshape((-1, 7))
        detections = detections[detections[:, 4] * detections[:, 6] >= conf_th]
        detections.append(detections)
    detections = np.concatenate(detections, axis=0)

    if len(detections) == 0:
        boxes = np.zeros((0, 4), dtype=np.int)
        scores = np.zeros((0,), dtype=np.float32)
        classes = np.zeros((0,), dtype=np.float32)
    else:
        box_scores = detections[:, 4] * detections[:, 6]

        # scale x, y, w, h from [0, 1] to pixel values
        old_h, old_w = img_h, img_w
        offset_h, offset_w = 0, 0
        if letter_box:
            if (img_w / input_shape[1]) >= (img_h / input_shape[0]):
                old_h = int(input_shape[0] * img_w / input_shape[1])
                offset_h = (old_h - img_h) // 2
            else:
                old_w = int(input_shape[1] * img_h / input_shape[0])
                offset_w = (old_w - img_w) // 2
        detections[:, 0:4] *= np.array(
            [old_w, old_h, old_w, old_h], dtype=np.float32)

        # NMS
        nms_detections = np.zeros((0, 7), dtype=detections.dtype)
        for class_id in set(detections[:, 5]):
            idxs = np.where(detections[:, 5] == class_id)
            cls_detections = detections[idxs]
            keep = _nms_boxes(cls_detections, nms_threshold)
            nms_detections = np.concatenate(
                [nms_detections, cls_detections[keep]], axis=0)

        xx = nms_detections[:, 0].reshape(-1, 1)
        yy = nms_detections[:, 1].reshape(-1, 1)
        if letter_box:
            xx = xx - offset_w
            yy = yy - offset_h
        ww = nms_detections[:, 2].reshape(-1, 1)
        hh = nms_detections[:, 3].reshape(-1, 1)
        boxes = np.concatenate([xx, yy, xx+ww, yy+hh], axis=1) + 0.5
        boxes = boxes.astype(np.int)
        scores = nms_detections[:, 4] * nms_detections[:, 6]
        classes = nms_detections[:, 5]
    return boxes, scores, classes
