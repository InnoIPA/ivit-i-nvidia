import os, logging, json
from typing import Tuple
from flask import current_app

DIV = "-"*3 + "\n"
FRAMEWORK_LIST = ['tensorrt', 'openvino' ]

def special_situation(model_cfg):
    """
    define custom situation for model_path and label path
    """
    def get_framework(model_cfg):
        if ("framework" in model_cfg.keys()):
            return model_cfg["framework"]
        else:
            for framework in FRAMEWORK_LIST:
                if framework in model_cfg.keys().lower():
                    return framework
    
    return True if get_framework(model_cfg)=="openvino" and model_cfg['tag']=="pose" else False    

def parse_task_info(path:str, pure_content:bool=False) -> Tuple[bool, tuple, str]:
    """
    Parsing the application informations and return the initialize status, error message and relative informations.
    
    - Input
        - path              : path to application folder
        - pure_content      : the task_cfg will merge to model_cfg when pure_content is False
    - Output
        - ret               : if application initailize failed the 'ret' will be False
        - task_cfg_path      : path to application configuration
        - model_cfg_path    : path to model configuration
        - task_cfg           : the content of application configuration with json format
        - model_cfg         : the content of model configuration with json format
        - err               : if application initailize failed the error message will push into 'err'.
    """
    # placeholder for each variable
    ret, task_cfg_path, model_cfg_path, task_cfg, model_cfg, err = False, None, None, None, None, ""
    
    # get the configuration path
    task_cfg_path = os.path.join( os.path.join(current_app.config["TASK_ROOT"], path), current_app.config["TASK_CFG_NAME"])
    
    # checking the application path
    if os.path.exists(task_cfg_path):
        task_cfg = load_json(task_cfg_path)
        framework = task_cfg["framework"]

        # capturing the model config path
        if "prim" in task_cfg.keys():
            model_cfg_path = task_cfg["prim"]["model_json"] if "model_json" in task_cfg["prim"] else None
        else:
            model_cfg_path = task_cfg["model_json"] if "model_json" in task_cfg else None
        if model_cfg_path != None:

            # cheching the model config path
            if os.path.exists(model_cfg_path):
                model_cfg = load_json(model_cfg_path)
                
                # the python api have to merge each config
                if not pure_content:
                    model_cfg.update(task_cfg)
                
                # checking the model path
                if "model_path" in model_cfg[framework]:
                    
                    if os.path.exists(model_cfg[framework]["model_path"]):
                        
                        # checking the label path
                        if special_situation(model_cfg):
                            ret=True
                        else:
                            if os.path.exists(model_cfg[framework]["label_path"]):
                                ret=True
                            else:
                                err = "Could not find the path to label ({})".format(model_cfg['label_path'])
                    else:
                        err = "Could not find the path to model ({})".format(model_cfg[framework]['model_path']) 
                else:
                    err = "Could not find the key of the model_path"
            else:
                err = "Could not find the model configuration's path ({})".format(model_cfg_path)
        else:
            err = "Could not find the key of the model configuration ({})".format("model_path")    
    else:
        err = "Could not find the path to application's configuration ({})".format(task_cfg_path)
    
    if err != "": logging.error(err)
    return ret, (task_cfg_path, model_cfg_path, task_cfg, model_cfg), err

# ------------------------------------------------------------------------------------------------------------------------------------------------------

def print_dict(input:dict):
    for key, val in input.items():
        print(key, val)


def load_json(path:str) -> dict:
    # --------------------------------------------------------------------
    # debug
    data = None
    if not os.path.exists(path):
        logging.error('File is not exists ! ({})'.format(path))
    elif os.path.splitext(path)[1] != '.json':
        logging.error("It's not a json file ({})".format(path))
    else:
        with open(path) as file:
            data = json.load(file)  # load is convert dict from json "file"
    return data

def write_json(path:str, data:dict):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)    # 縮排是4

def check_src_type(src:str) -> str:
    
    ret = ""
    map_table = {
        "camera":['dev', 'video'],
        "video":['mp4', 'avi'],
        "image":['jpg', 'png'],
        "rtsp":['rtsp'],
    }

    for key, val in map_table.items():
        for ext in val:
            if ext in src:
                ret = key

    return ret

def check_json(s):
    try:
        json.decode(s)
        return True
    except json.JSONDecodeError:
        return False

def print_route():
    logging.info("Call WEB API -> {}".format(request.path))