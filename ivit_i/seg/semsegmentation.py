import cv2, os, shutil, time, sys
import numpy as np
import logging
import tensorrt as trt
import copy

sys.path.append(f'{os.getcwd()}')
from ivit_i.utils.logger import config_logger
from ivit_i.utils.timer import Timer
from ivit_i.common import common
from ivit_i.common.common import Model
from ivit_i.common.process import preproc
from ivit_i.utils.parser import load_json, load_txt, parse_config

class SemSegmentation(Model):

    def __init__(self, idx):
        super(SemSegmentation, self).__init__(idx)

    """ Load model and setup global parameters """
    def load_model(self, config):
        config = parse_config(config)
        # parse information from configuration and get palette.
        (   self.input_size, self.out_size, self.preprocess, 
            self.thres, self.dynamic_shape ) = self.parse_param(config)
        
        # init engine
        engine_path = config['model_path']
        max_batch_size = -1 if self.dynamic_shape !=None else 1
        ([context, inputs, outputs, bindings, stream]) = self.init_engine(engine_path, max_batch_size)
        # clear context
        self.clear_runtime()
        # return trt_objects and palette
        palette = self.get_palette(config)
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
            "detections": [],                             # each object's information ( { xmin, ymin, xmax, ymax, label, score, id } ).
            "input_size": None,
        }

        temp_dets = {                      
            "xmin": None,                         
            "ymin": None,
            "xmax": None,
            "ymax": None,
            "mask": None
        }

        # parsing tensorrt objects
        [ context, inputs, outputs, bindings, stream ] = trt_objects    
        self.store_runtime()
        # pre-process
        pre_frame = preproc(image=frame.copy(), size=self.input_size[-2:], mode=self.preprocess, is_mean=False) 
        np.copyto(inputs[0].host, pre_frame.ravel())    # copy buffer into device

        # do inference.
        t_infer = Timer()
        results = common.do_inference(context, bindings=bindings, inputs=inputs, outputs=outputs, stream=stream, dynamic_shape=self.dynamic_shape)

        info['frame']=frame.copy()
        info['input_size']=self.input_size

        if results:

            masks_conf = results[0].reshape((self.input_size[1], self.input_size[2], -1))
            
            new_temp_dets = temp_dets.copy() #copy.deepcopy(temp_dets) 
            
            new_temp_dets['mask'] = masks_conf

            info['detections'].append(new_temp_dets)                        # update into ret['detections']
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
