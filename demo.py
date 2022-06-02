import os, sys, cv2, logging, argparse
import numpy as np
sys.path.append(os.getcwd())
from init_i.utils.logger import config_logger
from init_i.utils.parser import load_json, load_txt, parse_input_data
from init_i.utils.timer import Timer
from init_i.utils.drawing_tools import Draw, get_palette, draw_fps
from init_i.common import api

def main(args):

    # ----------------------------------------------------------------------------------------------------------------
    # 1. Initialize logger
    config_logger(log_name='init-i-nvidia.log', write_mode='w', level='debug')

    # ----------------------------------------------------------------------------------------------------------------
    # 2. Load and parse configuration
    app_conf = load_json(args.config)                       # load the configuration of the application
    model_conf = load_json(app_conf['prim']['model_json'])             # load the configuration of the AI model
    model_conf.update(app_conf)

    # ----------------------------------------------------------------------------------------------------------------
    # 3. Check the framework is tensorrt
    if app_conf['framework'].lower() != 'tensorrt':
        msg = 'Excepted a tensorrt platform, but got {}.'.format('tensorrt')
        logging.error(msg)
        raise Exception(msg)

    # ----------------------------------------------------------------------------------------------------------------
    # 4. Get the target API
    try:
        trg = api.get(model_conf)
    except Exception as e:
        raise Exception('LOAD API FAILED: {}'.format(e))
        
    draw = Draw()
    # ----------------------------------------------------------------------------------------------------------------
    # 5. Load and initialize model which return a list of objects for inference and the palette
    trt_objects, palette = trg.load_model(model_conf)
    
    # ----------------------------------------------------------------------------------------------------------------
    # 6. Start inference base on three mode
    source_type = parse_input_data(app_conf['source'])
    if source_type=='camera':        # Camera 
        
        cap = cv2.VideoCapture(app_conf['source'])

        if not cap.isOpened():
            msg = "Can't capture the device. ({})".format(source_type)
            logging.error(msg, stack_info=True)
        # -------------- camera start --------------
        while(cap.isOpened()):
        
            t_fps = Timer()
            ret, frame = cap.read()
            if not ret and frame==None: break  
            
            info = trg.inference(trt_objects, frame, model_conf)   
            
            # ===============================================================
            # Do something
            frame_draw = draw.draw_detections(info, palette, model_conf)

            frame_draw = draw_fps(frame_draw, int(1/(t_fps.get_cost_time())))
            # ===============================================================
            cv2.imshow('iVINNO', frame_draw)
            key = cv2.waitKey(1)
            if key==ord('q'): 
                break
            elif key==ord('c'):
                palette = get_palette(model_conf)
        # -------------- camera end --------------
        cap.release()
        cv2.destroyAllWindows()
        
    elif source_type=='video':       # Video 
    
        cap = cv2.VideoCapture(app_conf['source'])
        # -------------- video start --------------
        while(cap.isOpened()):
            t_fps = Timer()
            ret, frame = cap.read()
            if not ret and frame==None: break  

            info = trg.inference(trt_objects, frame, model_conf)   
            frame_draw = draw.draw_detections(info, palette, model_conf)
            frame_draw = draw_fps(frame_draw, int(1/(t_fps.get_cost_time())))

            cv2.imshow('iVINNO', frame_draw)
            key = cv2.waitKey(1)
            if key==ord('q'): 
                break
            elif key==ord('c'):
                palette = get_palette(model_conf)
        # -------------- video end --------------
        cap.release()
        cv2.destroyAllWindows()

    elif source_type == 'image':     # Single image 
        t_fps = Timer()
        frame = cv2.imread(app_conf['source'])
        if frame.any()==None:
            msg = "Can't read image. ({})".format(source_type)
            logging.error(msg, exc_info=True, stack_info=True)
        # -------------- start --------------
        info = trg.inference(trt_objects, frame, model_conf)   
        frame_draw = draw.draw_detections(info, palette, model_conf)
        fps = int(1/(t_fps.get_cost_time()))
        frame_draw = draw_fps(frame_draw, fps)
        
        while True:
            cv2.imshow('iVINNO', frame_draw)
            key = cv2.waitKey(1)
            if key==ord('s'):
                cv2.imwrite('./results.jpg', frame_draw)
            elif key==ord('c'):
                frame_draw = frame.copy()
                frame_draw = draw.draw_detections(info, get_palette(model_conf), model_conf)
                frame_draw = draw_fps(frame_draw, fps)        
            elif key==ord('q'):
                break
        # -------------- end --------------
        cv2.destroyAllWindows()
        
    else:                           # Format error
        msg = 'Excepted `source` is ["camera", "video", "image"]'
        logging.error(msg)
        raise Exception(msg)

if __name__ == "__main__":

    # 宣告外部參數
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='the path of configuration.')
    args = parser.parse_args()

    main(args)