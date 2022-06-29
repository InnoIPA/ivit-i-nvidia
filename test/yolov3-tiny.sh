cd /workspace
echo "Download ..." | boxes


FRAMEWORK="tensorrt"
TASK_PATH="./task/yolov3-tiny-sample/task.json"
MODEL_PATH="./task/yolov3-tiny-sample/yolov3-tiny-416.trt"

cd /workspace

if [[ ! -f $MODEL_PATH ]];then

    echo "Download ..." | boxes
    python3 /workspace/task/yolov3-tiny-sample/custom_download.py -m yolov3-tiny -s 416 -f /workspace/task/yolov3-tiny-sample

    echo "Converting ..." | boxes
    ./converter/yolo-converter.sh ./task/yolov3-tiny-sample/yolov3-tiny-416
fi

echo "Change GPU ..." | boxes
python3 ./test/update_first_gpu.py -f $FRAMEWORK -j $TASK_PATH

echo "Run ..." | boxes
python3 demo.py -c ${TASK_PATH} -s
