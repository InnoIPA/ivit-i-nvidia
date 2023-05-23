#!/bin/bash
# For Darknet Model

# Define Parameters
WS="/workspace"
source "${WS}/docker/utils.sh"
MODEL_TYPE=""
SIZE=""

FILE=$(realpath "$0")
ROOT=$(dirname "${FILE}")

# -----------------------------------------------------

DOWNLOAD_MODEL=true
DOWNLOAD_DATA=true
CONVERT_MODEL=true

script_name=$(basename "$0")
short=mdcn:s:
long=model,data,covert,name:,size:,support,help

read -r -d '' usage <<EOF
Usage:
	-m | --model	: Download model
	-d | --data		: Download data
	-c | --covert	: Convert model
	-n | --name		: Model name
	-s | --size		: Model size
	--support       : Show all model we support.
EOF

read -r -d '' support <<EOF
Support Model:

		Model Name	| Size |        	
	---------------------------
	yolov3			| 416  |
	yolov3-tiny		| 416  |
	yolov3-spp		| 416  |
	yolov4			| 416  |
	yolov4-tiny		| 416  |
	yolov4-csp		| 416  |
	yolov4-p5		| 416  |	
	yolov4x-mish	| 416  |
EOF

TEMP=$(getopt -o $short --long $long --name "$script_name" -- "$@")

eval set -- "${TEMP}"

while :; do
    case "${1}" in
        -m | --model       	) DOWNLOAD_MODEL=false;     shift 1 ;;
        -d | --data		  	) DOWNLOAD_DATA=false;      shift 1 ;;
        -c | --covert 		) CONVERT_MODEL=false;      shift 1 ;;
		-n | --name 		) MODEL_TYPE=$2;       		shift 2 ;;
		-s | --size 		) SIZE=$2;					shift 2 ;;
		--support           ) echo "${support}" 1>&2;   exit ;;
        --help            	) echo "${usage}" 1>&2;   	exit ;;
        --                	) shift;                 	break ;;
        *                 	) echo "Error parsing"; 	exit 1 ;;
    esac
done

if [[ ${DOWNLOAD_DATA} = true ]];then
	if [[ -z "$MODEL_TYPE" ]];then
		printd "Not set Download model name ! --support can show all model we support !" R
		exit
	fi
fi

if [[ ${DOWNLOAD_DATA} = true ]];then
	if [[ -z "$SIZE" ]];then
		printd "Not set Download model size ! --support can show all model we support !" R
		exit
	fi
fi
# Model
MODEL_NAME="${MODEL_TYPE}-${SIZE}"
MODEL_ROOT="${WS}/model/${MODEL_TYPE}"
if [ ! -d ${MODEL_ROOT} ];then mkdir -p ${MODEL_ROOT}; fi

# Combine Parameters
MODEL_PATH="${MODEL_ROOT}/${MODEL_NAME}.trt"

# Setup Running Script
DOWNLOAD_SCRIPT="${ROOT}/yolo_download.py"
MODIFTY_GPU_SCRIPT="${WS}/tools/update_first_gpu.py"
CONVERT_SCRIPT="${WS}/converter/yolo-converter.sh"

RUN_DOWNLOAD_DATA="${ROOT}/download_data.sh"
RUN_DOWNLOAD_MODEL="python3 ${DOWNLOAD_SCRIPT} -m ${MODEL_TYPE} -s ${SIZE} -f ${MODEL_ROOT}"
RUN_CONVERT="${WS}/converter/yolo-converter.sh ${MODEL_ROOT}/${MODEL_NAME} "
RUN_BUILD_PLUGIN="/workspace/plugins/build_plugin.sh"


# -----------------------------------------------------

# Move to Workspace
# cd $WS || exit

# -----------------------------------------------------

# Build Darknet Plugin
${RUN_BUILD_PLUGIN}

# Download data
if [[ ${DOWNLOAD_DATA} = true ]];then
	${RUN_DOWNLOAD_DATA}
    printd "Complete download data !" R
fi

# Download model

if [[ ${DOWNLOAD_MODEL} = true ]];then
	
	${RUN_DOWNLOAD_MODEL}
	
    printd "Complete download model !" R
fi


# Convert Model
if [[ ${CONVERT_MODEL} = true ]];then
	if [[ ! -f ${MODEL_PATH} ]];then
		printf "Convert Model"
		${RUN_CONVERT}
	else
		printf "Found Converted Model\n"
	fi
    printd "Complete convert model !" R
fi
