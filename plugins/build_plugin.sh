#!/bin/bash
printf "\n"
printf "# Build Plugin \n"
DIR="/workspace/plugins"
cd ${DIR}

ls $(pwd)
if [[ ! -f "libyolo_layer.so" ]]; then
    make clean && make > /dev/null 2>&1;
else
    echo "Plugin already exist"
fi
#     for FILE in "$DIR"/*
#     do
#         echo $FILE
#     done
#     echo "Plugin already exist";
# fi

