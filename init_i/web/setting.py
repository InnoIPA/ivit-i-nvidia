from flask import current_app
import json

class basic_setting(object):
    JSONIFY_PRETTYPRINT_REGULAR=True
    JSON_SORT_KEYS=False
    TASK_ROOT="./app"
    TASK_CFG_NAME="app.json"
    TASK=dict()
    UUID=dict()
    RE_UUID=dict()
    SRC=dict()
    ALLOWED_HOSTS = ['*']
    RE_SRC='0'

def load_config(json_path):
    """
    1. We provide multi-configurations and the basic_setting is disable to modify.
    2. To fit the json file, developer have to use from_file() not from_envver().
    3. Using "try except" in the highest level, not in here.
    """
    current_app.config.from_object(basic_setting)
    current_app.config.from_file( json_path, load=json.load )
