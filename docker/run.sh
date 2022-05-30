#!/bin/bash
source "$(dirname $(realpath $0))/utils.sh"

# ---------------------------------------------------------
# Set the default value of the getopts variable 
gpu="all"
port=""
project_name="init-i"
framework=""
version="latest"
magic=false
server=false

# Install pre-requirement
if [[ -z $(which jq) ]];then
    printd "Installing requirements .... " Cy
    sudo apt-get install jq -yqq
fi

# Variable
CONF="init-i.json"
FLAG=$(ls ${CONF} 2>/dev/null)
if [[ -z $FLAG ]];then
    CONF="${RUN_PWD}/${CONF}"
    FLAG=$(ls ${CONF} 2>/dev/null)
    if [[ -z $FLAG ]];then
        printd "Couldn't find configuration (${CONF})" Cy
        exit
    fi
else
    printd "Detected configuration (${CONF})" Cy
fi

# Parse information from configuration
project_name=$(cat ${CONF} | jq -r '.PROJECT')
version=$(cat ${CONF} | jq -r '.VERSION')
framework=$(cat ${CONF} | jq -r '.FRAMEWORK')

# ---------------------------------------------------------
# help
function help(){
	echo "Run the iNIT-I environment."
	echo
	echo "Syntax: scriptTemplate [-g|p|c|f|smh]"
	echo "options:"
	echo "g		select the target gpu."
	echo "p		run container with Web API, setup the web api port number."
	echo "f		Setup framework like [ nvidia, intel, xillinx ]."
	echo "v		Setup docker image version like [ v0.1, lastest ]."
	echo "s		Server mode for non vision user"
	echo "m		Print information with magic"
	echo "h		help."
}
while getopts "g:p:c:f:v:shm" option; do
	case $option in
		g )
			gpu=$OPTARG
			;;
		p )
			port=$OPTARG
			;;
		f )
			framework=$OPTARG
			;;
		s )
			server=true
			;;
		m )
			magic=true
			;;
		v )
			version=$OPTARG
			;;
		h )
			help
			exit
			;;
		\? )
			help
			exit
			;;
		* )
			help
			exit
			;;
	esac
done

# ---------------------------------------------------------
# Setup Masgic
if [[ ${magic} = true ]];then
	printf "Preparing magic ... "
	sudo apt-get install -qy boxes > /dev/null 2>&1
	printf "Done \n"
fi

# ---------------------------------------------------------
# Setup variable
docker_image=""
workspace=""
docker_name=""
mount_camera=""
mount_gpu="--gpus"
set_vision=""
command="bash"
web_api="./run_web_api.sh"
docker_image="${project_name}/${framework}:${version}"
workspace="/workspace"
docker_name="${project_name}-${framework}"

# ---------------------------------------------------------
# Check if image come from docker hub
hub_name="maxchanginnodisk/${docker_image}"
from_hub=$(check_image $hub_name)
echo "Checking Docker Hun Image: ${from_hub}"
if [[ from_hub -eq 0 ]];then
	echo "From Local"
else
	echo "From Docker Hub"
	docker_image=${hub_name}
fi
echo $docker_image

# ---------------------------------------------------------
# SERVER or DESKTOP MODE
if [[ ${server} = false ]];then
	mode="DESKTOP"
	set_vision="-v /etc/localtime:/etc/localtime:ro -v /tmp/.x11-unix:/tmp/.x11-unix:rw -e DISPLAY=unix${DISPLAY}"
	# let display could connect by every device
	xhost + > /dev/null 2>&1
else
	mode="SERVER"
fi

# ---------------------------------------------------------
# Combine Camera option
all_cam=$(ls /dev/video* 2>/dev/null)
cam_arr=(${all_cam})

for cam_node in "${cam_arr[@]}"
do
    mount_camera="${mount_camera} --device ${cam_node}:${cam_node}"
done

# ---------------------------------------------------------
# Combine gpu option
mount_gpu="${mount_gpu} device=${gpu}"

# ---------------------------------------------------------
# If port is available, run the WEB API
if [[ -n ${port} ]];then 
	# command="python3 ${web_api} --host 0.0.0.0 --port ${port} --af ${framework}"
	command="source ${web_api} -n ${framework_abbr} -b 0.0.0.0:${port} -t 10"
fi

# ---------------------------------------------------------
# Show information
title="\n\
PROGRAMMER: Welcome to iNIT-I \n\
FRAMEWORK:  ${framework}\n\
MODE:  ${mode}\n\
DOCKER: ${docker_image} \n\
CONTAINER: ${docker_name} \n\
PORT: ${port} \n\
CAMERA:  $((${#cam_arr[@]}/2))\n\
GPU:  ${gpu}\n\
COMMAND: ${command}"

print_magic "${title}" "${magic}"

# ---------------------------------------------------------
# Run container
docker_cmd="docker run \
--name ${docker_name} \
${mount_gpu} \
--rm -it \
--net=host --ipc=host \
-w ${workspace} \
-v `pwd`:${workspace} \
${mount_camera} \
${set_vision} \
${docker_image} \"${command}\""

# echo ""
# echo -e "Command: ${docker_cmd}"
# echo ""
bash -c "${docker_cmd}"
