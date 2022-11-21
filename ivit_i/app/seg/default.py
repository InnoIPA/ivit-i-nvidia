# Basic Application
import cv2, logging
import itertools as it
import numpy as np

# iVIT Libarary
from ivit_i.utils.parser import load_json
from ivit_i.app.common import ( 
    App, 
    DETS,
    FRAME,
    OUT_RESOL )

from ivit_i.utils.draw_tools import (
    CUSTOM_SCALE,
    PADDING,
    BASE_FONT_SIZE,
    BASE_FONT_THICK,
    get_text_size,
    get_scale,
    draw_text,
    draw_rect
)

IN_SIZE     = "input_size"
CUSTOM_SCALE = 0.5

# Main
class Default(App):

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        
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

    def init_draw_param(self, frame, trg_size):

        # if frame_size not None means it was already init 
        if( self.frame_size == None): 
            self.frame_size = frame.shape[:2]
            scale           = get_scale(frame) * CUSTOM_SCALE
            self.frame_size = frame.shape[:2]
            self.trg_scale  = max(BASE_FONT_SIZE*scale, 0)
            self.trg_thick  = max(int(BASE_FONT_THICK*scale), 1)
            self.padding    = int(PADDING*scale)
            ( w, h ), baseline = get_text_size( "Temp",                                    
                                                self.trg_scale, 
                                                self.trg_thick )
            self.text_wid, self.text_hei, self.text_base = w, h , baseline

        src_h, src_w = self.frame_size
        trg_h, trg_w = trg_size

        return (src_h/trg_h, src_w/trg_w)
    
    def create_color_map(self, color_palette):
        classes = np.array(color_palette, dtype=np.uint8)[:, ::-1] # RGB to BGR
        classes_num = len(classes)
        color_map = np.zeros((256, 1, 3), dtype=np.uint8)
        color_map[:classes_num, 0, :] = classes
        color_map[classes_num:, 0, :] = np.random.uniform(0, 255, size=(256-classes_num, 3))
        return color_map

    def apply_color_map(self, _input, color_map):
        color_map = self.create_color_map(color_map).astype(np.uint8)
        input_3d = cv2.merge([_input, _input, _input]).astype(np.uint8)
        return cv2.LUT(input_3d, color_map)

    # parse the mask
    def parse_mask(self, full_mask, mask, bbox, thres=0.5):
        
        # normalize
        mask = mask[1]
        mask += np.abs(np.min(mask))
        mask /= np.max(mask)                    
        
        # resize mask
        x1, y1, x2, y2 = bbox                   # bounding box with correct size.
        target_size = (x2-x1, y2-y1) 
        mask = cv2.resize( mask, target_size)       

        # set true and false depend on confidence
        mask = np.where(mask>=thres, 1, 0).astype(np.uint8)

        # Put the mask in the right location.
        full_mask[y1:y2, x1:x2] = mask
        return full_mask

    def __call__(self, frame, info, draw=True):
        
        self.text_draw = None
        scale_h, scale_w = self.init_draw_param(frame, info[IN_SIZE][1:])

        _mask = np.zeros(self.frame_size, dtype=np.uint8)
        
        for det in info[DETS]:  
            class_id, class_name, class_score = det['id'], det['label'], det['score']
            x1, x2, y1, y2 = det['xmin']*scale_w, det['xmax']*scale_w, det['ymin']*scale_h, det['ymax']*scale_h
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2] )

            
            content = '{}'.format(class_name)
            
            frame = draw_rect(
                    frame           = frame, 
                    left_top        = ( x1, y1 ), 
                    right_bottom    = ( x2, y2 ), 
                    color           = self.palette[class_name],
                    thick           = self.trg_thick )
            frame = draw_text(
                frame       = frame, 
                text        = content, 
                left_top    = (x1, y1), 
                color       = ( 0, 0, 0), 
                size        = self.trg_scale, 
                thick       = self.trg_thick, 
                start_from_top = False,
                outline     = True,
                background  = True,
                background_color = self.palette[class_name] )
        
            _mask = self.parse_mask(_mask, det['mask'], (x1, y1, x2, y2), thres=0.5)

        # only support list
        new_mask = self.apply_color_map(_mask, list(self.palette.values()))
        frame = np.floor_divide(frame, 2) + np.floor_divide(new_mask, 2)  # 向下取整 7/2=3

        return frame, self.text_draw
        