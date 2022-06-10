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

try:
    # ----------------------------------------------------
    # for trt_pose
    import torch, trt_pose
    from trt_pose.coco import coco_category_to_topology
    from trt_pose.parse_objects import ParseObjects
    from trt_pose.draw_objects import DrawObjects
except Exception as e:
    raise Exception(e)
# ----------------------------------------------------

class BodyPose(Model):
    """
    Set the place holder of topology, parser and drawer, all of them from trt-pose
    """
    def __init__(self, idx):
        super(BodyPose, self).__init__(idx)
        # human pose
        self.topology = None
        self.parser = None
        self.drawer = None
        self.engine = None

    def load_model(self, conf):
        
        conf = parse_config(conf)
        self.topology, self.parser, self.drawer = self.load_parser(conf)
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

    def inference(self, trt_objects, frame, conf):

        conf = parse_config(conf)
        # init
        out_resolution = conf["output_resolution"] if 'output_resolution' in conf.keys() else None # for display
        
        # tidy up the return information 
        info = {
            "frame": None,                          # placeholder for frame.
            "output_resolution": out_resolution,    # the resize proportion output resolution.
            "detections": []                              # each object's information ( { xmin, ymin, xmax, ymax, label, score, id } ).
        }
        temp_dets = {                      
            "drawer": None,
            "counts": None,
            "objects": None,
            "peaks": None,
            "xmin": None,
            "xmax": None,
            "ymin": None,
            "ymax": None,
        }

        # parsing tensorrt objects
        [ context, inputs, outputs, bindings, stream ] = trt_objects
        self.store_runtime()
        
        # pre-process
        pre_frame = preproc(image=frame.copy(), size=self.input_size[-2:], mode=self.preprocess) 
        pre_frame = np.expand_dims(pre_frame, axis=0)   # only need in trt_pose 
        np.copyto(inputs[0].host, pre_frame.ravel())    # copy buffer into device

        # do inference.
        t_infer = Timer()
        results = common.do_inference(context, bindings=bindings, inputs=inputs, outputs=outputs, stream=stream, dynamic_shape=self.dynamic_shape)

        # update frame into info['frame']
        info['frame']=frame.copy()

        # map each result into detections
        if results:

            # parse results
            counts, objects, peaks = self.parse_output(results)

            # put in info
            new_temp_dets = temp_dets.copy()
            new_temp_dets['drawer']=self.drawer
            new_temp_dets['counts']=np.array(counts)
            new_temp_dets['objects']=objects
            new_temp_dets['peaks']=peaks
            info['detections'].append(new_temp_dets)                        # update into ret['detections']
        # clear context
        self.clear_runtime()
        return info

    def load_parser(self, conf):
        """
        Load human pose parser ( label )
        * Input: conf
        * Output: topology, parser, drawer 
        """
        conf = parse_config(conf)
        human_pose = load_json(conf['label_path'])
        topology = coco_category_to_topology(human_pose)
        parser = ParseObjects(topology)
        drawer = DrawObjects(topology, alpha=0.3, border=5)
        return topology, parser, drawer

    def parse_param(self, conf):
        """
        Parse parameters from config
        * Input: conf
        * Output: input_size, out_size, preprocess, thres, dynamic_shape
        """
        conf = parse_config(conf)
        input_size = tuple(map(int, conf['input_size'].split(","))) # c, h, w
        out_size = [ input_size[1]//4, input_size[2]//4 ]
        preprocess = conf['preprocess']
        thres = float(conf['thres'])
        dynamic_shape = (1,)+input_size if 'dynamic_batch' in conf.keys() else None # setup with one batch -> ( 1, 3, h, w)

        return input_size, out_size, preprocess, thres, dynamic_shape

    def parse_output(self, results):
        """ 
        Parse the output which generated after inference 
        * Input: results
        * Output: counts, objects, peaks
        * Notice: you could search "counts, objects, peaks" online to figure out what's the mean of theme.
        """
        cmap, paf = results
        cmap = np.resize(cmap, (1, 18, self.out_size[0], self.out_size[1]) )
        paf = np.resize(paf, (1, 18, self.out_size[0], self.out_size[1]) )
        counts, objects, peaks = self.parser(torch.Tensor(cmap), torch.Tensor(paf)) # parse output
        return counts, objects, peaks

