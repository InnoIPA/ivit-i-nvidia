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

# https://drive.google.com/file/d/15e86j8KmctNE9HmpQGXxZ8CM7LHLKCSm/view?usp=sharing
NAME="innodisk_dram.avi"
GID="15e86j8KmctNE9HmpQGXxZ8CM7LHLKCSm"
download $GID ${NAME}