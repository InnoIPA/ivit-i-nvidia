# Yolov4-tiny: official yolov4 model trained from `DarkNet`

1. Enter the environment
    ```bash
    ./docker/run.sh -f nvidia -m
    ```
2. Download model
    ```bash
    # In the yolov4 folder
    cd /path/to/init-i/app/yolov4              # modify to your path
    python3 custom_download.py -m yolov4 -s 416 

    # In the init-i folder
    python3 ./app/yolov4/custom_download.py -m yolov4 -s 416 -f ./app/yolov4

    # The weight and config will be downloaded
    ls ./app/yolov4/yolov4-416*
    ./app/yolov4/yolov4-416.cfg  ./app/yolov4/yolov4-416.weights
    ```
3. Convert Model
    ```bash
    # For Example
    cd /path/to/init-i

    # Notice: no need to give extension here
    ./converter/yolo-converter.sh ./app/yolov4/yolov4-416

    # After convert yolov4-416 should be generated.
    ls ./app/yolov4/yolov4-416* | grep trt
    ./app/yolov4/yolov4-416.trt
    ```
    * Convert performance
      * `1050 Ti`
        * yolo to onnx: 8s
        * onnx to tensorrt: 1m 51s ( 111s )
4. Run demo.py
    ```
    cd /path/to/init-i
    python3 tensorrt_demo.py -c ./app/yolov4/task.json
    ```