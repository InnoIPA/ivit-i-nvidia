#!/bin/bash
source /workspace/tools/utils.sh

printd "Start to initialize Sample ..." BCy
echo -e "\
\n
Supported Samples: \n\
    - Classification \n\
    - YOLOv4 \n\
    - YOLOv4-tiny \n
    - parking-lot-detect \n\
    - traffic-flow-detect \n\
    - wrong-side-detect \n\
"

cd /workspace || exit

echo "-----------------------------------"
printd "Initialize Classification Sample" G
./test/classification.sh

echo "-----------------------------------"
printd "Initialize YOLOv4 Sample" G
./test/yolov4.sh

echo "-----------------------------------"
printd "Initialize YOLOv4-tiny Sample" G
./test/yolov4-tiny.sh

echo "-----------------------------------"
printd "Initialize parking-lot-detect" G
./test/parking-lot-detect.sh

echo "-----------------------------------"
printd "Initialize traffic-flow-detect" G
./test/traffic-flow-detect.sh

echo "-----------------------------------"
printd "Initialize wrong-side-detect" G
./test/wrong-side-detect.sh

echo "-----------------------------------"
printd "ALL DONE !" G
echo ""

VAR=$@
CMD="bash"

if [[ -n "$VAR" ]];then 
    CMD=$VAR; echo $CMD
fi

/bin/bash -c "$CMD"