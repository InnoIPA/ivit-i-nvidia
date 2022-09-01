# Copyright 2022 Max Chang
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
# --------------------------------------------------------------------------------
ROOT=$(dirname `realpath $0`)
cd $ROOT
source ./utils.sh
ROOT=`pwd`

# --------------------------------------------------------------------------------
# torch2trt
printd "$(date +"%T") Install torch2trt " Cy
TRG="torch2trt"

if [[ -n ${TRG} ]];then git clone https://github.com/NVIDIA-AI-IOT/torch2trt; fi
cd ${TRG}
python3 setup.py install --plugins
cd $ROOT && rm -rf ${TRG}

# --------------------------------------------------------------------------------
# TRT_POSE
# printd "$(date +%T) Check trt_pose " Cy
# TRG="pure_trt_pose"

# if [[ -n ${TRG} ]];then git clone https://github.com/p513817/pure_trt_pose.git; fi
# cd ${TRG}
# python3 setup.py install
# cd $ROOT && rm -rf ${TRG}

# # --------------------------------------------------------------------------------
# printd "DONE" Cy