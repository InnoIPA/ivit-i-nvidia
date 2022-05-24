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

TRG_FOLDER="./"

if [[ ! (${TRG_FOLDER} == *"${ROOT}"*) ]];then
	echo "$(date +"%F %T") Move terminal to $(realpath ${TRG_FOLDER})"
	cd ${TRG_FOLDER}
fi

# ------------------------------------------------------------------------------

# Model: https://drive.google.com/file/d/1qPC5ew1wQAmPKwKaodPT97mRzc3TYwKA/view?usp=sharing
NAME="yolov4-tiny-mask.weights"
GID="1qPC5ew1wQAmPKwKaodPT97mRzc3TYwKA"
download $GID ${NAME}

# https://drive.google.com/file/d/1ZsOfBJ-F6jN68o6ZwtdcZMrVFyojU-9p/view?usp=sharing
NAME="yolov4-tiny-mask.cfg"
GID="1ZsOfBJ-F6jN68o6ZwtdcZMrVFyojU-9p"
download $GID ${NAME}

# name: https://drive.google.com/file/d/1PNQffG4GV2h-C9TUZoMVv1PpeEzvSwir/view?usp=sharing
NAME="yolov4-tiny-mask.txt"
GID="1PNQffG4GV2h-C9TUZoMVv1PpeEzvSwir"
download $GID ${NAME}
