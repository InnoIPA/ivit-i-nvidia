
#!/bin/bash
# For Darknet Model

# Define Parameters
LEN=20
WS="/workspace"
FRAMEWORK="tensorrt"
TASK_ROOT="task"

TASK_NAME="innodisk_dram_detector"
TASK_CONF="task.json"
MODEL_NAME="yolov3-tiny-dram"

RUN_DEMO=false
SERVER_MODE=""

# Combine Parameters
TASK_PATH="${WS}/${TASK_ROOT}/${TASK_NAME}"
CONF_PATH="${TASK_PATH}/${TASK_CONF}"
MODEL_PATH="${TASK_PATH}/${MODEL_NAME}.trt"

# Setup Running Script
DOWNLOAD_SCRIPT="download_model.sh"
MODIFTY_GPU_SCRIPT="${WS}/docker/update_first_gpu.py"
CONVERT_SCRIPT="${WS}/converter/yolo-converter.sh"

RUN_DOWNLOAD_DATA="./task/innodisk_dram_detector/download_data.sh"
RUN_DOWNLOAD_MODEL="./task/innodisk_dram_detector/download_model.sh"
RUN_CONVERT="./converter/yolo-converter.sh ./task/innodisk_dram_detector/yolov3-tiny-dram "
RUN_GPU_MODIFY="python3 ${MODIFTY_GPU_SCRIPT} -f ${FRAMEWORK} -j ${CONF_PATH}"
RUN_BUILD_PLUGIN="/workspace/plugins/build_plugin.sh"

# Title
printf "\n"
printf "# FAST-RUN ${TASK_NAME} \n"

# Define HELP
function help(){
	echo "Run the iVIT-I environment."
	echo
	echo "Syntax: scriptTemplate [-rsh]"
	echo "options:"
	echo "r     run demo"
    echo "s     run demo with server mode"
	echo "h     help."
}

# Define Argument and Parse it
while getopts "rsh" option; do
	case $option in
		r )
			RUN_DEMO=true ;;
		s )
			SERVER_MODE="-s" ;;
		h )
			help; exit ;;
		\? )
			help; exit;;
		* )
			help; exit;;
	esac
done

# Show information
printf "%-${LEN}s | %-${LEN}s \n" "TIME" "$(date)"
printf "%-${LEN}s | %-${LEN}s \n" "TASK_PATH" "${TASK_PATH}"
printf "%-${LEN}s | %-${LEN}s \n" "CONF_PATH" "${CONF_PATH}"
printf "%-${LEN}s | %-${LEN}s \n" "RUN SAMPLE" "${RUN_DEMO}"
printf "%-${LEN}s | %-${LEN}s \n" "SERVER MODE" $(if [[ ${SERVER_MODE} = "" ]];then echo false; else echo true;fi)
printf "%-${LEN}s | %-${LEN}s \n" "DOWNLOAD DATA" "${RUN_DOWNLOAD_DATA}"
printf "%-${LEN}s | %-${LEN}s \n" "DOWNLOAD MODEL" "${RUN_DOWNLOAD_MODEL}"
printf "%-${LEN}s | %-${LEN}s \n" "MODIFY GPU" "${RUN_GPU_MODIFY}"
printf "%-${LEN}s | %-${LEN}s \n" "CONVERT MODEL" "${RUN_CONVERT}"
printf "%-${LEN}s | %-${LEN}s \n" "BUILD PLUGIN" "${RUN_BUILD_PLUGIN}"

# Move to Workspace
cd $WS

# Build Darknet Plugin
${RUN_BUILD_PLUGIN}

# Download data
${RUN_DOWNLOAD_DATA}

# Download model
${RUN_DOWNLOAD_MODEL}

# Convert Model
if [[ ! -f ${MODEL_PATH} ]];then
	printf "Convert Model"
	${RUN_CONVERT}
else
	printf "Found Converted Model"
fi

# Change GPU
${RUN_GPU_MODIFY}

# Run Sample
if [[ "$RUN_DEMO" = true ]];then
	printf "Run Sample ... \n"
	python3 demo.py -c ${CONF_PATH} ${SERVER_MODE}
else
	printf "End"
fi