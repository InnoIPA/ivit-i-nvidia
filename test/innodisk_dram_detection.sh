cd /workspace
echo "Download ..." | boxes
./task/innodisk_dram_detector/download_model.sh
./task/innodisk_dram_detector/download_testing_data.sh

echo "Converting ..." | boxes
./converter/yolo-converter.sh ./task/innodisk_dram_detector/yolov3-tiny-dram

echo "Run ..." | boxes
python3 demo.py -c ./task/innodisk_dram_detector/task.json -s