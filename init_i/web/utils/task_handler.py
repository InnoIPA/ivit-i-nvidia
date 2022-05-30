import sys, os, shutil, time, logging, copy, uuid
from typing import Tuple
from flask import current_app

from .parser import parse_task_info
from .src_handler import init_src
from .app_handler import init_task_app
from .uuid import gen_uuid
DIV = '-'*30
def get_tasks() -> list:
    """ 
    取得所有 APP：這邊會先進行 INIT 接著在透過 ready 這個 KEY 取得是否可以運行，最後回傳 ready, failed 兩個 List 
    """
    ret = { 
            "ready": [],
            "failed": [] 
        }
    # init all apps
    for idx, task in enumerate(os.listdir(current_app.config['TASK_ROOT'])):

        task_status, task_uuid, task_info = init_tasks(task, index=idx)
    
        # parse ready and failed applications
        ret["ready" if task_status=="stop" else "failed"].append({
            "framework": task_info['framework'], 
            "name": task_info['name'], 
            "uuid": task_uuid, 
            "status": task_status, 
            "error": task_info['error'], 
            "model_path": task_info['model_path'] if "model_path" in task_info else None,
            "application": task_info['application'] if "application" in task_info else None,
        })
    return ret

def init_tasks(task_name:str, fix_uuid:str=None, index=None) -> Tuple[bool, str]:
    """ 
    Initialize each application, the UUID, application will be generated.
    """
    [ logging.info(cnt) for cnt in [ DIV, f"[{index}] Start to initialize application ({task_name})"] ]

    # UUID
    task_path = os.path.join( current_app.config["TASK_ROOT"], task_name )
    task_uuid = gen_uuid(name=task_name, len=8)
    if (task_name in current_app.config["UUID"].values()) and ( fix_uuid == None ):             
        # no need to initialize application if UUID is already exists
        logging.debug("UUID ({}) had already exist.".format(task_uuid))
    else:
        if fix_uuid != None:
            task_uuid = fix_uuid
            logging.debug("Fixed UUID hash table! {}:{}".format(task_name, task_uuid))
        else:
            current_app.config["UUID"].update( { task_uuid: task_name } )
            logging.debug("Update UUID hash table! {}:{}".format(task_uuid, task_name))

    # Parse the information about this task
    ret, (app_cfg_path, model_cfg_path, app_cfg, model_cfg), err = parse_task_info(task_name)
    task_status = "stop" if ret else "error"
    task_framework = app_cfg["framework"] if ret else None

    # Update basic information
    current_app.config["TASK"].update({ 
        task_uuid:{ 
            "name": task_name,
            "framework": task_framework, 
            "path": task_path,
            "status": task_status, 
            "error": err,
    }})
    
    # If initialize success 
    #   * parse the category and application
    #   * model have to relative with application
    #   * so, we have to capture the model information, which model is been used by which uuid.
    if task_status != "error":

        # Update information
        logging.debug("Update information to uuid ({})".format(task_uuid))
        current_app.config["TASK"][task_uuid].update({    
            "application": model_cfg["application"],
            "model_path": f"{model_cfg[task_framework]['model_path']}",     # path to model
            "label_path": f"{model_cfg[task_framework]['label_path']}",     # path to label 
            "config_path": f"{model_cfg_path}",             # path to model config
            "device": f"{model_cfg[task_framework]['device']}",
            "source" : f"{app_cfg['input_data']}",
            "output": None,
            "api" : None,       # api
            "runtime" : None,   # model or trt_obj
            "config" : model_cfg,    # model config
            "draw_tools" : None,
            "palette" : None, 
            "status" : "stop", 
            "cur_frame" : 0,
            "fps": None,
            "stream": None 
        })
        
        # Create new source if source is not in global variable
        init_src(   task_uuid, 
                    app_cfg['input_data'], 
                    app_cfg['input_type'] if 'input_type' in app_cfg.keys() else None   )
        
        # Update the application mapping table: find which UUID is using the application
        init_task_app(  task_uuid,  
                        app_cfg     ) 

        logging.info('Create the global variable for "{}" (uuid: {}) '.format(task_name, task_uuid))
    else:
        logging.error('Failed to create the application ({})'.format(task_name))
    
    return (task_status, task_uuid, current_app.config['TASK'][task_uuid])