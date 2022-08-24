#!/bin/bash
source /workspace/docker/utils.sh

printd "Start to initialize Sample ..." BCy
echo -e "\
\n
Supported Samples: \n\
    - Classification \n\
    - YOLOv4 \n\
    - YOLOv4-tiny \n"
cd /workspace

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
printd "Initialize Innodisk DRAM Sample" G
./test/innodisk_dram_detection.sh

echo "-----------------------------------"
printd "ALL DONE !" G
echo ""
