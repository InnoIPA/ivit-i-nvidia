import json
import logging, subprocess
from flask import Blueprint, abort, jsonify, current_app
from init_i.web.utils import get_address, get_gpu_info, get_v4l2

bp_utils = Blueprint('utils', __name__)

@bp_utils.route("/v4l2/")
def web_v4l2():
    return jsonify(get_v4l2())

@bp_utils.route("/device/")
def web_device_info():
    if current_app.config["FRAMEWORK"]=="nvidia":
        return jsonify(get_gpu_info())
    else:
        return jsonify("Intel device")

@bp_utils.route("/source")
def web_source():
    return jsonify( current_app.config["SRC"] )