
FRAMEWORK="tensorrt"
TASK_PATH="./task/people_seg_sample/task.json"
MODEL_PATH="./task/people_seg_sample/peoplesegnet.engine"

cd /workspace

if [[ ! -f $MODEL_PATH ]]; then

    echo "Download ..." | boxes
    ./task/people_seg_sample/download_model.sh

    echo "Converting ..." | boxes
    ./converter/tao-converter -k nvidia_tlt \
    -d 3,576,960 \
    -o mask_fcn_logits/Conv2D,mask_fcn_logits/BiasAdd \
    -e /workspace/task/people_seg_sample/peoplesegnet.engine \
    -t fp32 \
    -i nchw \
    -m 1 \
    /workspace/task/people_seg_sample/peoplesegnet_resnet50.etlt
fi

echo "Change GPU ..." | boxes
python3 ./test/update_first_gpu.py -f $FRAMEWORK -j $TASK_PATH

echo "Run ..." | boxes
python3 demo.py -c ${TASK_PATH} -s
