
FRAMEWORK="tensorrt"
TASK_PATH="./task/humanpose_sample/task.json"
MODEL_PATH="./task/humanpose_sample/resnet18_baseline_att_224x224_A.engine"

cd /workspace

if [[ ! -f $MODEL_PATH ]]; then

    echo "Download ..." | boxes
    ./task/humanpose_sample/download_model.sh

    echo "Converting ..." | boxes
    ./converter/pose-converter \
    -m ./task/humanpose_sample/resnet18_baseline_att_224x224_A.pth \
    -j ./task/humanpose_sample/label.json \
    -e ./task/humanpose_sample/resnet18_baseline_att_224x224_A.engine

fi

echo "Change GPU ..." | boxes
python3 ./test/update_first_gpu.py -f $FRAMEWORK -j $TASK_PATH

echo "Run ..." | boxes
python3 demo.py -c ${TASK_PATH} -s
