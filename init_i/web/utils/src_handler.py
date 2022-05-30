import logging
from flask import current_app
from .parser import check_src_type

def init_src(task_uuid, source, source_type=None):
    """ 
    Initialize Source: 
        1. Update to app.config['SRC']
        2. Append the uuid into app.config['SRC'][{source}]["proc"]         # means process
        3. Check is the source is exist ( support v4l2 and any file, but excepted rtsp ... )
    """
    
    if not (source in current_app.config["SRC"].keys()):
        logging.info("Update source information")
        # Update information
        current_app.config["SRC"].update({ 
            f"{source}" : { 
                "status": "stop",
                "proc": [],
                "type": source_type if source_type != None else check_src_type(source),
                "object": None,
                "detail": "",
            }
        })
        # Add process into config
        if not ( task_uuid in current_app.config['SRC'][ source ]['proc'] ):
            logging.debug("Update process into source config")
            current_app.config['SRC'][ source ]['proc'].append(task_uuid)
        else:
            logging.debug("Process already in the source config, please check app.config['SRC']['proc']")
        
        # Clear process which unused
        [ current_app.config['UUID'].pop(uuid, None) for uuid in current_app.config['SRC'][ source ]['proc'] if not (uuid in current_app.config['UUID']) ]
        
    else:
        logging.info("Source is already exists ({})".format(source))

    