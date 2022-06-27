#!/bin/bash
echo "$(date +"%F %T") Download model from NVIDIA NGC ..."
ROOT=$(dirname `realpath ${0}`)
FILE="peoplesegnet_resnet50.etlt"

echo $ROOT
cd $ROOT

if [[ -f "${FILE}" ]];then
    echo "File is exists !!"
else
    # model
    wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/peoplesegnet/versions/deployable_v2.0.1/files/peoplesegnet_resnet50.etlt
    # label
    wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/peoplesegnet/versions/deployable_v2.0.1/files/peoplesegnet_resnet50_int8.txt
fi

