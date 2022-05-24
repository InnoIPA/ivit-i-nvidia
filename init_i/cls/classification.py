import cv2, os, shutil, time, sys
import numpy as np
import logging
import tensorrt as trt

sys.path.append(f'{os.getcwd()}')
from init_i.utils.logger import config_logger
from init_i.utils.timer import Timer
from init_i.common import common
from init_i.common.common import Model
from init_i.common.process import preproc
from init_i.utils.parser import load_json, load_txt, parse_config

class Classification(Model):

    def __init__(self, idx):
        super(Classification, self).__init__(idx)

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

        # tidy up the return information 
        info = {
            "frame": None,                          # placeholder for frame.
            "output_resolution": out_resolution,    # the resize proportion output resolution.
            "dets": []                              # each object's information ( { xmin, ymin, xmax, ymax, label, score, id } ).
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
        pre_frame = preproc(image=frame.copy(), size=self.input_size[-2:], mode=self.preprocess) 
        np.copyto(inputs[0].host, pre_frame.ravel())    # copy buffer into device

        # do inference.
        t_infer = Timer()
        results= common.do_inference(context, bindings=bindings, inputs=inputs, outputs=outputs, stream=stream, dynamic_shape=self.dynamic_shape)
        
        # update frame into info['frame']
        info['frame']=frame.copy()

        # map each result into dets
        if results:
            for result in results:              # parse each result after classification
                result = self.custom_norm(result)
                new_temp_dets = temp_dets.copy() 
                new_temp_dets['id'] = int(np.argmax(result))
                new_temp_dets['score'] = float( result[ new_temp_dets['id'] ])
                new_temp_dets['label'] = labels[ new_temp_dets['id'] ]
                info['dets'].append(new_temp_dets)                               # update into ret['dets']
        
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
