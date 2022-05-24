#!/bin/bash

function printd(){
    echo -e "[$(date --rfc-3339=seconds)] ${1}"
}

# Basic
MODEL=$(realpath $1)

# Check file is exists
FLAG=$(ls ${MODEL} 2> /dev/null)
if [[ -z $FLAG ]];then
    printd "Couldn't find model (${MODEL})"
    exit
fi

# Build the shared object
printd "Build plugins ... "
cd plugins && make clean >/dev/null && make >/dev/null
cd ..
printd "Darknet plugins are ready"

# Convert Model
printd "YOLO 2 ONNX ... "
python3 ./plugins/darknet-yolo/yolo_to_onnx.py -m "${MODEL}" >/dev/null
printd "YOLO 2 ONNX ... Done"

printd "ONNX 2 TensorRT ... "
python3 ./plugins/darknet-yolo/onnx_to_tensorrt.py -m "${MODEL}" > /dev/null
printd "ONNX 2 TensorRT ... Done"