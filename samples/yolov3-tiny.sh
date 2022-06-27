cd /workspace
echo "Download ..." | boxes
python3 ./task/yolov3-tiny-sample/custom_download.py -m yolov3-tiny -s 416 -f ./task/yolov3-tiny-sample

echo "Converting ..." | boxes
./converter/yolo-converter.sh ./task/yolov3-tiny-sample/yolov3-tiny-416

echo "Run ..." | boxes
python3 demo.py -c ./task/yolov3-tiny-sample/task.json