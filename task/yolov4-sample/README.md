# Yolov4-tiny: official yolov4 model trained from `DarkNet`

1. Enter the environment
    ```bash
    sudo ./docker/run.sh -m
    ```
2. Download model
    ```bash
    # In the yolov4 folder
    cd /path/to/init-i/task/yolov4              # modify to your path
    python3 custom_download.py -m yolov4 -s 416 

    # In the init-i folder
    python3 ./task/yolov4-sample/custom_download.py -m yolov4 -s 416 -f ./task/yolov4-sample

    # The weight and config will be downloaded
    ls ./task/yolov4-sample/yolov4-416*
    ./task/yolov4-sample/yolov4-416.cfg  ./task/yolov4-sample/yolov4-416.weights
    ```
3. Convert Model
    ```bash
    # For Example
    cd /path/to/init-i

    # Notice: no need to give extension here
    ./converter/yolo-converter.sh ./task/yolov4-sample/yolov4-416

    # After convert yolov4-416 should be generated.
    ls ./task/yolov4-sample/yolov4-416* | grep trt
    ./task/yolov4-sample/yolov4-416.trt
    ```
    * Convert performance
      * `1050 Ti`
        * yolo to onnx: 8s
        * onnx to tensorrt: 1m 51s ( 111s )
4. Run demo.py
    ```
    cd /path/to/init-i
    python3 demo.py -c ./task/yolov4-sample/task.json
    ```