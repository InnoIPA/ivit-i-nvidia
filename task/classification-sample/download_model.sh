#!/bin/bash

function download(){
	ID=$1
	NAME=$2

	if [[ ! -z $(ls model 2>/dev/null )  ]];then
		echo "$(date +"%F %T") the model folder has already exist !"
	else
		gdown --id $ID -O $NAME
	fi
}

# ------------------------------------------------------------------------------

echo "$(date +"%F %T") Download model from google drive ..."
ROOT=$(dirname `realpath ${0}`)
echo $ROOT
cd $ROOT

TRG_FOLDER="/workspace/model"
if [[ ! -d ${TRG_FOLDER} ]];then
	mkdir ${TRG_FOLDER}
fi

if [[ ! (${TRG_FOLDER} == *"${ROOT}"*) ]];then
	echo "$(date +"%F %T") Move terminal to $(realpath ${TRG_FOLDER})"
	cd ${TRG_FOLDER} || exit
fi

# ------------------------------------------------------------------------------

FOLDER='resnet'
ZIP='resnet34.zip'
MODEL="resnet34.onnx"
LABEL="imagenet.txt"


# Create & Move Folder
if [[ ! -d ${FOLDER} ]];then mkdir ${FOLDER}; fi
cd ${FOLDER} || exit

# Download Model
if [[ -f "${MODEL}" ]];then
	echo "$(date +"%F %T") Model already exist"
else
	# ZIP: https://drive.google.com/file/d/12A_K6zuQ1PfooA7OP7ZcfZ1YVg1Oxo4l/view?usp=share_link
	GID="12A_K6zuQ1PfooA7OP7ZcfZ1YVg1Oxo4l"
	download $GID ${ZIP}
	unzip ${ZIP} && mv *.onnx ${MODEL}
fi

# Download Model
if [[ -f "${LABEL}" ]];then
	echo "$(date +"%F %T") Label already exist"
else
	# Model: https://drive.google.com/file/d/13nmiw_RbZ_pHVUOh9pnD0razxhWhKV6C/view?usp=share_link
	GID="13nmiw_RbZ_pHVUOh9pnD0razxhWhKV6C"
	download $GID ${LABEL}
fi



