#!/bin/bash

function printd(){
    echo -e "[$(date --rfc-3339=seconds)] ${1}"
}

# Basic
MODEL=$(realpath $1)
PLUGIN="/workspace/plugins/libyolo_layer.so"

# Check file is exists
FLAG=$(ls "${MODEL}.weights" 2> /dev/null)
if [[ -z $FLAG ]]; then
    printd "Couldn't find model ( ${MODEL}.weights )"
    exit
fi

if [[ -f "${MODEL}.trt" ]]; then
    printd "TensorRT Engine Already Exist !"; exit
fi

# Build the shared object
if [[ ! -f "${PLUGIN}" ]]; then
    printd "Build plugins ... "
    cd plugins && make clean >/dev/null && make >/dev/null
    cd ..
fi
printd "Darknet plugins are ready"

# Convert Model
printd "YOLO 2 ONNX ... "
python3 /workspace/plugins/darknet-yolo/yolo_to_onnx.py -m "${MODEL}"
printd "YOLO 2 ONNX ... Done"

printd "ONNX 2 TensorRT ... "
python3 /workspace/plugins/darknet-yolo/onnx_to_tensorrt.py -m "${MODEL}"
printd "ONNX 2 TensorRT ... Done"