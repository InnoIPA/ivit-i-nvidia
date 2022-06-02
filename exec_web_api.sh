#!/bin/bash

# Install pre-requirement
if [[ -z $(which jq) ]];then
    echo "Installing requirements .... "
    sudo apt-get install jq -yqq
fi

# Variable
CONF="init-i.json"
FLAG=$(ls ${CONF} 2>/dev/null)
if [[ -z $FLAG ]];then
    CONF="${RUN_PWD}/${CONF}"
    FLAG=$(ls ${CONF} 2>/dev/null)
    if [[ -z $FLAG ]];then
        echo "Couldn't find configuration (${CONF})"
        exit
    fi
fi

# Parse information from configuration
echo "Detected configuration (${CONF})"
PORT=$(cat ${CONF} | jq -r '.PORT')
WORKER=$(cat ${CONF} | jq -r '.WORKER')
THREADING=$(cat ${CONF} | jq -r '.THREADING')
export INIT_I=/workspace/init-i.json

# Run
gunicorn --worker-class eventlet \
-w ${WORKER} \
--threads ${THREADING} \
--bind 0.0.0.0:${PORT} \
init_i.web.app:app
