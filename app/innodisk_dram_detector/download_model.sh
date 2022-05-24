#!/bin/bash

function download(){
	ID=$1
	NAME=$2

	if [[ -f $NAME ]];then
		echo "$(date +"%F %T") $NAME is exists !"
	else
		gdown --id $ID -O $NAME
	fi
}

# ------------------------------------------------------------------------------

echo "$(date +"%F %T") Download model from google drive ..."
ROOT=$(dirname `realpath ${0}`)
echo $ROOT
cd $ROOT
# ------------------------------------------------------------------------------

# Model: https://drive.google.com/file/d/1bZ0ylEEwMKhdEb3y04Ajxx3pLbhcAJ_A/view?usp=sharing
NAME="yolov3-tiny-dram.weights"
GID="1bZ0ylEEwMKhdEb3y04Ajxx3pLbhcAJ_A"
download $GID ${NAME}

# https://drive.google.com/file/d/1tuHz-3jKuo0a2Hl8rVgUJgqXdhEJc9mq/view?usp=sharing
NAME="yolov3-tiny-dram.cfg"
GID="1tuHz-3jKuo0a2Hl8rVgUJgqXdhEJc9mq"
download $GID ${NAME}

# name: https://drive.google.com/file/d/156L0xi-b__eLIUn72b6bctrZwU3q-VgE/view?usp=sharing
NAME="yolov3-tiny-dram.txt"
GID="156L0xi-b__eLIUn72b6bctrZwU3q-VgE"
download $GID ${NAME}
