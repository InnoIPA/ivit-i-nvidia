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

# 6.1 Model: https://drive.google.com/file/d/1Umpdjvna5pCezrq_j8i6ABnhYfRVBCtY/view?usp=sharing
# NAME="usb.engine"
# GID="1Umpdjvna5pCezrq_j8i6ABnhYfRVBCtY"
# download $GID ${NAME}

# Model ( Etlt ): https://drive.google.com/file/d/18pQvtLNkR-b4VVdXx_ud8f-Xm768kFSG/view?usp=sharing
NAME="yolov4_darknet53_e100_pruned_fp16.etlt"
GID="18pQvtLNkR-b4VVdXx_ud8f-Xm768kFSG"
download $GID ${NAME}

# Label: https://drive.google.com/file/d/17OXNVr9VPdovK3v9JXzak3C5g8qWlJYY/view?usp=sharing
NAME="usb.txt"
GID="17OXNVr9VPdovK3v9JXzak3C5g8qWlJYY"
download $GID ${NAME}
