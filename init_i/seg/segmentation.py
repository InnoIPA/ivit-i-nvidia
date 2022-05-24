import cv2, os, shutil, time, sys
import numpy as np
import logging
import tensorrt as trt
import copy

sys.path.append(f'{os.getcwd()}')
from init_i.utils.logger import config_logger
from init_i.utils.timer import Timer
from init_i.common import common
from init_i.common.common import Model
from init_i.common.process import preproc
from init_i.utils.parser import load_json, load_txt, parse_config

class Segmentation(Model):

    def __init__(self, idx):
        super(Segmentation, self).__init__(idx)

    """ Load model and setup global parameters """
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
    
    """ Do Inference """
    def inference(self, trt_objects, frame, conf):
        conf = parse_config(conf)
        out_resolution = conf["output_resolution"] if 'output_resolution' in conf.keys() else None
        labels = load_txt(conf['label_path'])

        # tidy up the return information 
        info = {
            "frame": None,                          # placeholder for frame.
            "output_resolution": out_resolution,    # the resize proportion output resolution.
            "dets": [],                             # each object's information ( { xmin, ymin, xmax, ymax, label, score, id } ).
            "input_size": None,
        }

        temp_dets = {                      
            "xmin": None,                         
            "ymin": None,
            "xmax": None,
            "ymax": None,
            "label": None,                      # the placeholder for label.
            "score": None,                      # the placeholder for probability.
            "id": None,                         # the placeholder for the indext with the maxmium value.
            "mask": None
        }

        # parsing tensorrt objects
        [ context, inputs, outputs, bindings, stream ] = trt_objects    
        
        # pre-process
        pre_frame = preproc(image=frame.copy(), size=self.input_size[-2:], mode=self.preprocess) 
        np.copyto(inputs[0].host, pre_frame.ravel())    # copy buffer into device
        self.store_runtime()
        # do inference.
        t_infer = Timer()
        results = common.do_inference(context, bindings=bindings, inputs=inputs, outputs=outputs, stream=stream, dynamic_shape=self.dynamic_shape)

        info['frame']=frame.copy()
        info['input_size']=self.input_size
        
        if results:

            ress = np.reshape(results[0], (100, 6))
            img_masks = np.reshape(results[1], (100, 2 ,28, 28))
            
            for idx, res in enumerate(ress):

                bboxes, label_id, score = res[:4], res[4], res[5]

                if score>self.thres:

                    new_temp_dets = temp_dets.copy() #copy.deepcopy(temp_dets) 
                    y1, x1, y2, x2 = map(float, bboxes) # parse the result after classification                    
                    new_temp_dets['xmin'] = x1
                    new_temp_dets['xmax'] = x2
                    new_temp_dets['ymin'] = y1
                    new_temp_dets['ymax'] = y2
                    new_temp_dets['id'] = int(label_id)
                    new_temp_dets['label'] = labels[new_temp_dets['id']]
                    new_temp_dets['score'] = float(score)
                    new_temp_dets['mask'] = img_masks[idx]

                    info['dets'].append(new_temp_dets)                        # update into ret['dets']
        # clear context
        self.clear_runtime()
        return info

    """ Parse parameters from config """
    def parse_param(self, conf):
        conf = parse_config(conf)

        input_size = tuple(map(int, conf['input_size'].split(","))) # c, h, w
        out_size = [ 28, 28 ]
        preprocess = conf['preprocess']
        thres = float(conf['thres'])
        dynamic_shape = (1,)+input_size if 'dynamic_batch' in conf.keys() else None # setup with one batch -> ( 1, 3, h, w)

        return input_size, out_size, preprocess, thres, dynamic_shape
