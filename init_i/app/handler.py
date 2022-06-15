
import logging
APP_KEY = "application"
FRAMEWORK = "tensorrt"

def get_application(config:dict):
    
    if not APP_KEY in config:
        raise Exception("Could not find the {}".format(APP_KEY))
    
    app_config = config[APP_KEY]
    app_name = app_config['name']
    depend_label = None

    if not 'depend_on' in app_config:
        # capture all label list
        logging.info('Get all labels for {}'.format(APP_KEY))
        try:
            depend_label = get_labels(config)
        except Exception as e:
            logging.error(e)
        
    else:
        depend_label = app_config['depend_on'] if type(app_config['depend_on'])==list else [ app_config['depend_on'] ]

    logging.warning(type(depend_label))
    logging.warning(depend_label)

    if 'counting' in app_name:
        from .counting import Counting as trg
    elif 'direction' in app_name:
        from .moving_direction import MovingDirection as trg
    
    return trg(depend_label)
            
def get_labels(config:dict) -> list:
    """ get the label file and capture all category in it """
    content = []
    with open(config[FRAMEWORK]["label_path"], 'r') as f:
        for line in f.readlines():
            content.append(line.strip('\n'))
    return content