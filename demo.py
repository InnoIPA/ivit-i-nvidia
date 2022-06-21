import os, sys, cv2, logging, argparse
import numpy as np
sys.path.append(os.getcwd())
from init_i.utils.logger import config_logger
from init_i.utils.parser import load_json, load_txt, parse_input_data
from init_i.utils.timer import Timer
from init_i.utils.drawing_tools import Draw, get_palette, draw_fps
from init_i.common import api
from init_i.web.ai.pipeline import Source
from init_i.app.handler import get_application

CV_WIN='Detection Results'

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
    source_type = parse_input_data(model_conf['source'])

    src = Source(model_conf['source'], model_conf['source_type'])

    has_application=True
    
    try:
        application = get_application(model_conf)
        if application == None:
            has_application = False
    except Exception as e:
        logging.error(e)
        has_application=False
    
    cv2.namedWindow(CV_WIN, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(CV_WIN, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret_frame, frame = src.get_frame()
        if not ret_frame:
            if model_conf["source_type"] in ['Image', 'V4L2']:
                break
            elif model_conf["source_type"] in ['Video', 'RTSP']:
                src = Source(model_conf['source'], model_conf['source_type'])
                continue

        org_frame = frame.copy()
        info = trg.inference(trt_objects, org_frame, model_conf)   
        
        if info is not None:
            if not has_application:
                frame = draw.draw_detections(info, palette, model_conf)
            else:
                frame = application(org_frame, info)
        else:
            continue
        
        cv2.imshow(CV_WIN, frame)
    
        key = cv2.waitKey(1)
        if key in {ord('q'), ord('Q'), '27'}:
            break

    src.release()


if __name__ == "__main__":

    # 宣告外部參數
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='the path of configuration.')
    args = parser.parse_args()

    main(args)