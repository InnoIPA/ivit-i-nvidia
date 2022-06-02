
# Install pre-requirement
if [[ -z $(which jq) ]];then
    printd "Installing requirements ... jq " Cy
    sudo apt-get update
    sudo apt-get install jq -yqq
fi
if [[ -z $(which netstat) ]];then
    printd "Installing requirements ... net-tools " Cy
    sudo apt-get update
    sudo apt-get install net-tools -yqq
fi

# Parse information from configuration
CONF="init-i.json"
port=$(cat ${CONF} | jq -r '.PORT')
netstat -ano | grep :${port}