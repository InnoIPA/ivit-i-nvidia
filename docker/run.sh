#!/bin/bash
source "$(dirname $(realpath $0))/utils.sh"

# Set the default value of the getopts variable 
GPU="all"
RUN_WEB=true
RUN_CLI=false
MAGIC=true
SERVER=false
INIT=false
FIRST_TIME=true
LOG="./docker/docker_info.log"

# Install pre-requirement
if [[ -z $(which jq) ]];then
    printd "Installing requirements .... " Cy
    sudo apt-get install jq -yqq
fi

# Check configuration is exit
CONF="ivit-i.json"
FLAG=$(ls ${CONF} 2>/dev/null)
if [[ -z $FLAG ]];then
	printd "Couldn't find configuration (${CONF})" Cy
	exit
else
    printd "Detected configuration (${CONF})" Cy
fi

# Parse information from configuration
PROJECT=$(cat ${CONF} | jq -r '.PROJECT')
VERSION=$(cat ${CONF} | jq -r '.VERSION')
PLATFORM=$(cat ${CONF} | jq -r '.PLATFORM')
PORT=$(cat ${CONF} | jq -r '.PORT')

# Help
function help(){
	echo "Run the iVIT-I environment."
	echo
	echo "Syntax: scriptTemplate [-g|wsmih]"
	echo "options:"
	echo "g		select the target GPU."
	echo "s		Server mode for non vision user."
	echo "c		Run as command line mode"
	echo "m		Print information with MAGIC."
	echo "i		Initialize docker container ( start over )."
	echo "h		help."
}

while getopts "g:wcsihmh" option; do
	case $option in
		g )
			GPU=$OPTARG ;;
		s )
			SERVER=true ;;
		c )
			RUN_CLI=true ;;
		m )
			MAGIC=false ;;
		i )
			INIT=true ;;
		h )
			help; exit ;;
		\? )
			help; exit ;;
		* )
			help; exit ;;
	esac
done

# Setup Masgic package
if [[ ${MAGIC} = true ]];then
	if [[ -z $(which boxes) ]];then 
		printd "Preparing MAGIC "
		sudo apt-get install -qy boxes > /dev/null 2>&1; 
	fi
fi

# Setup variable
DOCKER_IMAGE="${PROJECT}-${PLATFORM}:${VERSION}"
DOCKER_NAME="${PROJECT}-${PLATFORM}"

MOUNT_CAMERA=""
MOUNT_GPU="--gpus"

WORKSPACE="/workspace"
SET_VISION=""
RUN_WEB_CMD="./exec_web_api.sh"
INIT_CMD="./init_for_sample.sh"
RUN_CMD="$( if [[ ${RUN_CLI} = false ]];then echo "${RUN_WEB_CMD}";else echo "bash";fi )"

# Initialize docker container and check is the first time
if [[ ${INIT} = true ]];then
	printd "Initialize docker container" Cy
	docker rm ${DOCKER_NAME}
	RUN_CMD="${INIT_CMD} && ${RUN_CMD}"
else
	FIRST_TIME=false
fi


# Check if image come from docker hub
DOCKER_HUB_IMAGE="maxchanginnodisk/${DOCKER_IMAGE}"
if [[ ! $(check_image $DOCKER_HUB_IMAGE) -eq 0 ]];then
	DOCKER_IMAGE=${DOCKER_HUB_IMAGE}
	echo "From Docker Hub ... Update Docker Image Name: ${DOCKER_IMAGE}"
fi

# SERVER or DESKTOP MODE
if [[ ${SERVER} = false ]];then
	mode="DESKTOP"
	SET_VISION="-v /tmp/.x11-unix:/tmp/.x11-unix:rw -e DISPLAY=unix${DISPLAY}"
	# let display could connect by every device
	xhost + > /dev/null 2>&1
else
	mode="SERVER"
fi

# Combine Camera option
all_cam=$(ls /dev/video* 2>/dev/null)
cam_arr=(${all_cam})

for cam_node in "${cam_arr[@]}"
do
	MOUNT_CAMERA="${MOUNT_CAMERA} --device ${cam_node}:${cam_node}"
done

# Combine GPU option
MOUNT_GPU="${MOUNT_GPU} device=${GPU}"

# Combine docker RUN_CMD line
DOCKER_CMD="docker run \
--name ${DOCKER_NAME} \
${MOUNT_GPU} \
-it \
--net=host --ipc=host \
-v /etc/localtime:/etc/localtime:ro \
-w ${WORKSPACE} \
-v `pwd`:${WORKSPACE} \
${MOUNT_CAMERA} \
${SET_VISION} \
${DOCKER_IMAGE} \"${RUN_CMD}\" \n"

# Show information
INFO="\n\
PROGRAMMER: Welcome to ${PROJECT} \n\
FRAMEWORK:  ${PLATFORM}\n\
MODE:  ${mode}\n\
DOCKER: ${DOCKER_IMAGE} \n\
CONTAINER: ${DOCKER_NAME} \n\
Web API: ${RUN_WEB} \n\
HOST: 0.0.0.0:${PORT} \n\
MOUNT_CAMERA:  $((${#cam_arr[@]}/2))\n\
GPU:  ${GPU}\n\
COMMAND: ${RUN_CMD} \n"

# Print the INFO
print_magic "${INFO}" "${MAGIC}"
echo -e "Command: ${DOCKER_CMD}"

# Log
printf "$(date +%m-%d-%Y)" > "${LOG}"
printf "${INFO}" >> "${LOG}"
printf "\nDOCKER COMMAND: \n${DOCKER_CMD}" >> "${LOG}";

# Check is the container alread exit
if [[ $(check_container ${DOCKER_NAME}) -eq 0 ]];then
	
	# Run container
	bash -c "${DOCKER_CMD}";

else
	printd "Found container ... " Cy
	
	xhost + 2 > /dev/null;

	if [ "$( docker container inspect -f '{{.State.Running}}' $DOCKER_NAME )" == "true" ]; then
		printd "Docker container is running" Cy
		if [[ ${RUN_CLI} = true ]]; then
			docker exec -it ${DOCKER_NAME} ${RUN_CMD};	
		else
			docker attach ${DOCKER_NAME};
		fi
	else
		if [[ ${RUN_CLI} = true ]]; then
			printd "Start docker container with command line mode" Cy
			docker start ${DOCKER_NAME};
			docker exec -it ${DOCKER_NAME} ${RUN_CMD};		
		else
			printd "Start docker container" Cy
			docker start ${DOCKER_NAME} -a;
		fi
	fi
fi