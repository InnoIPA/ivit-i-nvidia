
FRAMEWORK="tensorrt"
TASK_PATH="./task/classification_sample/task.json"
MODEL_PATH="./task/classification_sample/resnet50.engine"
cd /workspace

if [[ ! -f $MODEL_PATH ]];then
    echo "Download ..." | boxes
    python3 /workspace/task/classification_sample/download_resnext50.py
fi

echo "Change GPU ..." | boxes
python3 ./test/update_first_gpu.py -f $FRAMEWORK -j $TASK_PATH

echo "Run ..." | boxes
python3 demo.py -c ${TASK_PATH} -s