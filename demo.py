import os, sys, cv2, logging, argparse
from pyexpat import model
from shutil import ExecError
import numpy as np
sys.path.append(os.getcwd())
from ivit_i.utils.logger import config_logger
from ivit_i.utils.parser import load_json, load_txt, parse_input_data
from ivit_i.utils.timer import Timer
from ivit_i.utils.drawing_tools import Draw, get_palette, draw_fps
from ivit_i.common import api
from ivit_i.web.ai.pipeline import Source
from ivit_i.app.handler import get_application
from ivit_i.web.tools.common import handle_exception

CV_WIN='Detection Results'

def main(args):

    # 1. Initialize logger
    config_logger(log_name='ivit-i-nvidia.log', write_mode='w', level='debug')

    # 2. Load and combine configuration
    app_conf = load_json(args.config)                       # load the configuration of the application
    model_conf = load_json(app_conf['prim']['model_json'])             # load the configuration of the AI model
    total_conf = model_conf.copy()
    total_conf.update(app_conf)

    # 3. Get the target API and Draw tool
    try:
        trg = api.get(total_conf)
        draw = Draw()
    except Exception as e:
        handle_exception(error=e, title="Could not get ivit-i API", exit=True)

    # 4. Load and initialize model which return a list of objects for inference and the palette
    try:
        trt_objects, palette = trg.load_model(total_conf)
    except Exception as e:
        handle_exception(error=e, title="Could not load AI model", exit=True)

    # 5. Start inference base on three mode
    src = Source(total_conf['source'], total_conf['source_type'])

    # 6. Setting Application
    has_app=False
    try:
        application = get_application(total_conf)
        has_app = False if application == None else True

        # Setup parameter if needed
        app_info = total_conf["application"]

        # Area detection: point_points
        if "area" in app_info["name"]:
            key = "area_points"
            if not key in app_info: application.set_area(pnts=None, frame=src.get_first_frame())
            else: application.set_area(pnts=app_info[key])   

    except Exception as e:
        handle_exception(error=e, title="Could not load application ... set app to None", exit=False)
        has_app=False
    
    # 7. Start inference
    
    # server mode: won't display cv window
    if not args.server:
        cv2.namedWindow(CV_WIN, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(CV_WIN, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    try:
        while True:

            # 7.1. capture frame from source object
            ret_frame, frame = src.get_frame()
            
            # 7.2. if not frame break
            if not ret_frame: 
                if src.get_type().lower() in ["rtsp", "video"]:
                    src = Source(total_conf['source'], total_conf['source_type'])
                    continue

            # 7.3. do inference
            org_frame = frame.copy()
            info = trg.inference(trt_objects, org_frame, total_conf)   

            # 7.4. draw results or using application
            if not args.server:
                
                if info is None: continue

                # using default draw tool if no application available
                if not has_app:
                    frame = draw.draw_detections(info, palette, total_conf)
                else:
                    frame = application(org_frame, info)

                # show the results            
                cv2.imshow(CV_WIN, frame)
                key = cv2.waitKey(1 if not args.debug else 0)
                if key in {ord('q'), ord('Q'), '27'}:
                    break 

            else:
                logging.info( info["detections"])

    except KeyboardInterrupt:
        logging.warning("Quit")
    finally:        
        # release if needed
        trg.release()
        if not args.server: src.release()


if __name__ == "__main__":

    # 宣告外部參數
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='the path of configuration.')
    parser.add_argument('-d', '--debug', action="store_true", help='the debug mode.')
    parser.add_argument('-s', '--server', action="store_true", help='the server mode.')
    args = parser.parse_args()

    main(args)
