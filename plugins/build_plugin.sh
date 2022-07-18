#!/bin/bash
printf "\n"
printf "# Build Plugin \n"

cd /workspace/plugins
if [[ -z "libyolo_layer.so" ]];then
    make clean && make > /dev/null 2>&1;
else
    echo "Plugin already exist";
fi

