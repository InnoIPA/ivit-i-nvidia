import logging, copy
from flask import Blueprint, abort, jsonify, current_app
from init_i.web.utils import get_address, get_gpu_info, get_v4l2

bp_tasks = Blueprint('task', __name__)

@bp_tasks.route("/task/")
@bp_tasks.route("/tasks/")
def entrance():
    return jsonify(current_app.config["TASK_LIST"])

@bp_tasks.route("/task/<uuid>/")
def task_info(uuid):
    return jsonify(current_app.config['TASK'][uuid])

@bp_tasks.route("/task/<uuid>/info")
def task_simple_info(uuid):
    af = current_app.config['TASK'][uuid]["framework"]
    status = current_app.config['TASK'][uuid]['status']
    
    simple_config = {
        "framework": af, 
        "application": current_app.config['TASK'][uuid]['application'],
        "app_name": current_app.config['TASK'][uuid]['name'], 
        "source": current_app.config['TASK'][uuid]['source'], 
        "input_type": current_app.config['TASK'][uuid]['config']['input_type'], 
        "device": current_app.config['TASK'][uuid]['device'] ,
        "thres": current_app.config['TASK'][uuid]['config'][af]['thres'],
        "status": status,
    }
    return jsonify(simple_config)
