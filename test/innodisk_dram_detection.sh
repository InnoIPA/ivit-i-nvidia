
FRAMEWORK="tensorrt"
TASK_PATH="./task/innodisk_dram_detector/task.json"
MODEL_PATH="./task/innodisk_dram_detector/yolov3-tiny-dram.trt"

cd /workspace

if [[ ! -f $MODEL_PATH ]]; then
    echo "Download ..." | boxes
    ./task/innodisk_dram_detector/download_model.sh
    ./task/innodisk_dram_detector/download_testing_data.sh

    echo "Converting ..." | boxes
    ./converter/yolo-converter.sh ./task/innodisk_dram_detector/yolov3-tiny-dram
fi

echo "Change GPU ..." | boxes
python3 ./test/update_first_gpu.py -f $FRAMEWORK -j $TASK_PATH

echo "Run ..." | boxes
python3 demo.py -c ${TASK_PATH} -s
