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

# https://drive.google.com/file/d/1LdJRmvx5wvHsJxlrUzzp15V1yG21ZCXX/view?usp=sharing
NAME="output.mp4"
GID="1LdJRmvx5wvHsJxlrUzzp15V1yG21ZCXX"
download $GID ${NAME}