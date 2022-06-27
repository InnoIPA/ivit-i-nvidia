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
NAME_1="resnet18_baseline_att_224x224_A"


G_ID_1="1XYDdCUdiF2xxx4rznmLb62SdOUZuoNbd"

MODEL_1="${NAME_1}.pth"

ENG_1="${NAME_1}.engine"

		
download $G_ID_1 ${MODEL_1}