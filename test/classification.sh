#!/bin/bash

# Define Parameters
LEN=20
WS="/workspace"
FRAMEWORK="tensorrt"
TASK_ROOT="task"

TASK_NAME="classification-sample"
TASK_CONF="task.json"

# -----------------------------------------------------

RUN_DEMO=false
MODE=""
RTSP_ROUTE=""
SHOW_LIST=false


script_name=$(basename "$0")
short=t:ldsr
long=task:,route:,list,demo,server,rtsp,help

read -r -d '' usage <<EOF
Usage:
	-t | --task		: define task name
	-l | --list		: show available task name
	-d | --demo		: run demo ( display cv window )
	-s | --server	: run server mode ( only show log )
	-r | --rtsp		: run rtsp mode ( rtsp://127.0.0.0:8554/mystream )
	--route			: define rtsp route, ( rtsp://127.0.0.0:8554/<route> ) 
EOF

TEMP=$(getopt -o $short --long $long --name "$script_name" -- "$@")

eval set -- "${TEMP}"

while :; do
    case "${1}" in
        -t | --task       	) TASK_NAME=$2;             shift 2 ;;
        -d | --demo		  	) RUN_DEMO=true;           	shift 1 ;;
        -s | --server 		) MODE='-s';       			shift 1 ;;
		-r | --rtsp 		) MODE='-r';       			shift 1 ;;
		-l | --list 		) SHOW_LIST=true;			shift 1 ;;
		--route				) RTSP_ROUTE=$2;			shift 2 ;;
        --help            	) echo "${usage}" 1>&2;   	exit ;;
        --                	) shift;                 	break ;;
        *                 	) echo "Error parsing"; 	exit 1 ;;
    esac
done

# Move to Workspace
cd ${WS} || exit

if [[ "$SHOW_LIST" = true ]];then
	echo -e "\nList Tasks"
	ls "/workspace/task" | tr "" "\n" | nl
	exit 0
fi

# -----------------------------------------------------

# Combine Parameters
TASK_PATH="${WS}/${TASK_ROOT}/${TASK_NAME}"
CONF_PATH="${WS}/${TASK_ROOT}/${TASK_NAME}/${TASK_CONF}"

DOWNLOAD_SCRIPT="download_model.sh"
MODIFTY_GPU_SCRIPT="${WS}/tools/update_first_gpu.py"

RUN_DOWNLOAD_DATA="${TASK_PATH}/download_data.sh"
RUN_DOWNLOAD_MODEL="${TASK_PATH}/${DOWNLOAD_SCRIPT}"

RUN_GPU_MODIFY="python3 ${MODIFTY_GPU_SCRIPT} -f ${FRAMEWORK} -j ${CONF_PATH}"

# Show information
printf "%-${LEN}s | %-${LEN}s \n" "TIME" "$(date)"
printf "%-${LEN}s | %-${LEN}s \n" "TASK_PATH" "${TASK_PATH}"
printf "%-${LEN}s | %-${LEN}s \n" "CONF_PATH" "${CONF_PATH}"
printf "%-${LEN}s | %-${LEN}s \n" "RUN SAMPLE" "${RUN_DEMO}"
printf "%-${LEN}s | %-${LEN}s \n" "MODE" "${MODE}"
printf "%-${LEN}s | %-${LEN}s \n" "RTSP_ROUTE" "${RTSP_ROUTE}"
printf "%-${LEN}s | %-${LEN}s \n" "DOWNLOAD MODEL" "${RUN_DOWNLOAD_MODEL}"
printf "%-${LEN}s | %-${LEN}s \n" "MODIFY GPU" "${RUN_GPU_MODIFY}"

# Download data
${RUN_DOWNLOAD_DATA}

# Download model
${RUN_DOWNLOAD_MODEL}

# Convert Model
MODEL_PATH="/workspace/model/resnet/resnet34.trt"
if [[ ! -f ${MODEL_PATH} ]];then
	trtexec \
	--onnx=/workspace/model/resnet/resnet34.onnx \
	--batch=1 \
	--saveEngine=${MODEL_PATH}
fi

# Change GPU
${RUN_GPU_MODIFY}

# Run Sample
if [[ "$RUN_DEMO" == false ]];then printf "%s Initialize finished \n" "${TASK_NAME}"; exit 0 ; fi

# Title
printf "\n# RUN Sample: %s \n" "${TASK_NAME}"

export IVIT_I=/workspace/ivit-i.json

CMD="/workspace/demo.py -c ${CONF_PATH} ${MODE}"

if [[ "${RTSP_ROUTE}" != "" ]];then CMD="${CMD} -n ${RTSP_ROUTE}" ;fi

bash -c "$CMD"