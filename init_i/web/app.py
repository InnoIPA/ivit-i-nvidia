# ------------------------------------------------------------------------------------------
# common module
import cv2, time, logging, shutil, subprocess, base64, threading, os, sys, copy, json

# flask basic, socketio, filename and docs ( flasgger )
from flask import Flask, Blueprint, jsonify, request, render_template, url_for, redirect, abort
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from flasgger import Swagger
# flask, Corss-Origin Resource Sharing, avoid "No 'Access-Control-Allow-Origin' header"
from flask_cors import CORS as cors
# green flask and application
import eventlet
eventlet.monkey_patch()  

# init_i 
sys.path.append(os.getcwd())
from init_i.utils.logger import config_logger
from init_i.web.utils import get_address, get_tasks
from init_i.web.api import basic_setting, bp_utils, bp_tasks, bp_tests
# ------------------------------------------------------------------------------------------

def create_app():
    
    # initialize
    app = Flask(__name__)
    
    # loading configuration
    if not ('INIT_I' in os.environ.keys()):
        raise KeyError("Could not find the environ \"INIT_I\", please setup the custom setting path: $ export INIT_I=/workspace/init-i.json")
    else:
        app.config.from_object(basic_setting)
        app.config.from_file( os.environ["INIT_I"], load=json.load )

    # define logger
    config_logger(log_name=app.config['LOGGER'], write_mode='a', level='debug', clear_log=True)

    # update ip address
    if app.config['HOST']=="":
        addr = get_address()
        app.config['HOST']=addr
        logging.info('Update HOST to {}'.format(addr))

    # something important
    cors(app)                                                                   # share resource
    socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins='*')   # define socket
    swagger = Swagger(app)                                                      # define web api docs

    # register blueprint
    app.register_blueprint(bp_utils)
    app.register_blueprint(bp_tasks)
    app.register_blueprint(bp_tests)

    # define the web api
    @app.before_first_request
    @app.route("/reset/")
    def first_time():
        """ loading the tasks at first time or need to reset, the uuid and relatived information will be generated at same time."""
        logging.info("Start to initialize task and generate uuid for each task ... ")
        
        [ app.config[key].clear() for key in [ "TASK", "UUID", "TASK_LIST", "APPLICATION" ] if key in app.config ]
                
        try:
            app.config["TASK_LIST"]=get_tasks()
            return app.config["TASK_LIST"], 200
        except Exception as e:
            return "Initialize Failed ({})".format(e), 400

    @app.route("/", methods=["GET"])
    def index():
        """ return task list """
        return jsonify(app.config["TASK_LIST"])


    @app.route("/routes/", methods=["GET", "POST"])
    def help():
        routes = {}
        for r in app.url_map._rules:
            routes[r.rule] = {}
            routes[r.rule]["functionName"] = r.endpoint
            routes[r.rule]["methods"] = list(r.methods)

        routes.pop("/static/<path:filename>")
        return jsonify(routes)

    @app.route("/<key>/", methods=["GET"])
    def return_config(key):
        key_lower, key_upper = key.lower(), key.upper()
        if key_lower in app.config.keys():
            return jsonify( app.config[key_lower] ), 200
        elif key_upper in app.config.keys():
            return jsonify( app.config[key_upper] ), 200
        else:
            return "Unexcepted Route ( Please check /routes )", 400

    return app, socketio

if __name__ == "__main__":
    
    app, socketio = create_app()
    socketio.run(app, host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])