#!/bin/bash
function printd(){            
    
    if [ -z $2 ];then COLOR=$REST
    elif [ $2 = "G" ];then COLOR=$GREEN
	elif [ $2 = "BG" ];then COLOR=$BGREEN
	elif [ $2 = "R" ];then COLOR=$RED
    elif [ $2 = "BR" ];then COLOR=$BRED
	elif [ $2 = "Y" ];then COLOR=$YELLOW
    elif [ $2 = "BY" ];then COLOR=$BYELLOW
    elif [ $2 = "Cy" ];then COLOR=$Cyan
    elif [ $2 = "BCy" ];then COLOR=$BCyan
    else COLOR=$REST
    fi

    echo -e "$(date +"%y:%m:%d %T") ${COLOR}$1${REST}"
}
# Define Parameters
LEN=20
# WS="/workspace"
DOWNLOAD_MODEL=true
DOWNLOAD_DATA=true
CONVERT_MODEL=true
# -----------------------------------------------------
FILE=$(realpath "$0")
ROOT=$(dirname "${FILE}")

function help(){
	echo "Run the classification demo prework."
	echo
	echo "Syntax: scriptTemplate [-g|mdc]"
	echo "options:"
	echo "m		download model."
	echo "d		download data."
	echo "c		convert  model."
	echo "h		help."
}

while getopts "g:mdch:" option; do
	case $option in
		m )
			DOWNLOAD_MODEL=false ;;
		l )
			DOWNLOAD_DATA=false ;;
		c )
			CONVERT_MODEL=false ;;
		h )
			help; exit ;;
		\? )
			help; exit ;;
		* )
			help; exit ;;
	esac
done

# Move to Workspace
# cd ${WS} || exit

# -----------------------------------------------------

# Combine Parameters
DOWNLOAD_SCRIPT="download_model.sh"

RUN_DOWNLOAD_DATA="${ROOT}/download_data.sh"
RUN_DOWNLOAD_MODEL="${ROOT}/${DOWNLOAD_SCRIPT}"

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

    MODEL_PATH="/workspace/model/resnet/resnet34.trt"
    if [[ ! -f ${MODEL_PATH} ]];then
        /usr/src/tensorrt/bin/trtexec \
        --onnx=/workspace/model/resnet/resnet34.onnx \
        --saveEngine=${MODEL_PATH}
    fi
    printd "Complete convert model !" R
fi

