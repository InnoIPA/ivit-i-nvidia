from flask import current_app

"""
This application not the flask application
"""

APP_KEY = 'APPLICATION'

def init_task_app(task_uuid, app_cfg):
    
    if not ( APP_KEY in current_app.config ):
        # update app.config['APPLICATION'] if needed
        current_app.config.update({ APP_KEY: dict() })                            

    for app in app_cfg[APP_KEY.lower()]:
        if not (app in current_app.config[APP_KEY]): 
            current_app.config[APP_KEY].update( { app : list() } )          # update app.config['APPLICATION'][ {application}] 
        if not (task_uuid in current_app.config[APP_KEY][app]): 
            current_app.config[APP_KEY][app].append(task_uuid)              # update app.config['APPLICATION'][ {application}][ {UUID}] 
            