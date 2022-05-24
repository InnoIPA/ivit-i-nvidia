#!/bin/bash

# model
wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/peoplesegnet/versions/deployable_v2.0.1/files/peoplesegnet_resnet50.etlt

# label
wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/peoplesegnet/versions/deployable_v2.0.1/files/peoplesegnet_resnet50_int8.txt