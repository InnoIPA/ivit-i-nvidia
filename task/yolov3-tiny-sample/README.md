# Yolov3-tiny: official yolov3-tiny model trained from `DarkNet`

1. Enter the environment
    ```bash
    sudo ./docker/run.sh -m
    ```
2. Download model
    ```bash
    # In the yolov3-tiny folder
    cd /path/to/init-i/task/yolov3-tiny              # modify to your path
    python3 custom_download.py -m yolov3-tiny -s 416 

    # In the init-i folder
    python3 ./task/yolov3-tiny-sample/custom_download.py -m yolov3-tiny -s 416 -f ./task/yolov3-tiny-sample

    # The weight and config will be downloaded
    ls ./task/yolov3-tiny-sample/yolov3-tiny-416*
    ./task/yolov3-tiny-sample/yolov3-tiny-416.cfg  ./task/yolov3-tiny-sample/yolov3-tiny-416.weights
    ```
3. Convert Model
    ```bash
    # For Example
    cd /path/to/init-i

    # Notice: no need to give extension here
    ./converter/yolo-converter.sh ./task/yolov3-tiny-sample/yolov3-tiny-416

    # After convert yolov3-tiny-416 should be generated.
    ls ./task/yolov3-tiny-sample/yolov3-tiny-416* | grep trt
    ./task/yolov3-tiny-sample/yolov3-tiny-416.trt
    ```
    * Convert performance
      * `1050 Ti`
        * yolo to onnx: 2s
        * onnx to tensorrt: 32s
4. Run demo.py
    ```
    cd /path/to/init-i
    python3 demo.py -c ./task/yolov3-tiny-sample/task.json
    ```