# Basic Application
import cv2, logging
import itertools as it

# TRT Pose Estimation
try:
    from trt_pose.coco import coco_category_to_topology
    from trt_pose.draw_objects import DrawObjects
except Exception as e:
    logging.error(e); raise Exception(e)

# iVIT Libarary
from ivit_i.utils.parser import load_json
from ivit_i.app.common import ( 
    App, 
    DETS )

# Main
class Default(App):

    def __init__(self, config: dict) -> None:
        super().__init__(config)

        self.palette = self.get_palette(config)
        self.drawer = self.init_drawer(config)
        
        logging.info("Get Defualt Application")
    
    def get_params(self) -> dict:
        """ Define Counting Parameter Format """
        
        # Define Dictionary
        ret = {
            "name": self.def_param("string", "tracking", "define application name"),
        }
        
        # Console Log
        logging.info("Get The Basic Parameters of Application")
        for key, val in ret.items():
            logging.info("\t- {}".format(key))
            [ logging.info("\t\t- {}: {}".format(_key, _val)) for _key, _val in val.items() ]    
        return ret

    def init_drawer(self, config):
        """
        Load human pose parser ( label )
        * Input: config
        * Output: topology, parser, drawer 
        """
        topology = coco_category_to_topology(load_json(config['label_path']))
        drawer = DrawObjects(topology, alpha=0.3, border=5)
        return drawer

    def __call__(self, frame, info, draw=True):

        # Capture all center point in current frame and draw the bounding box
        for idx in it.count(0):
            
            # Check if interation over the length
            if idx >= (len(info[DETS])): break

            # Get Detection Object
            detection   = info[DETS][idx]
            frame = self.drawer(frame, detection['counts'], detection['objects'], detection['peaks'], self.palette)
            # _frame = draw_sth(_frame, 'COUNTS', int(detection['counts']))

        return frame, self.text_draw
        