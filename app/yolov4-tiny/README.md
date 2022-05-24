# Yolov4-tiny: official yolov4-tiny model trained from `DarkNet`

1. Enter the environment
    ```bash
    ./docker/trt/run.sh -f trt -m
    ```
2. Download model
    ```bash
    # In the yolov4-tiny folder
    cd /path/to/init-i/app/trt/yolov4-tiny              # modify to your path
    python3 custom_download.py -m yolov4-tiny -s 416 

    # In the init-i folder
    python3 ./app/trt/yolov4-tiny/custom_download.py -m yolov4-tiny -s 416 -f ./app/trt/yolov4-tiny

    # The weight and config will be downloaded
    ls ./app/trt/yolov4-tiny/yolov4-tiny-416*
    ./app/trt/yolov4-tiny/yolov4-tiny-416.cfg  ./app/trt/yolov4-tiny/yolov4-tiny-416.weights
    ```
3. Convert Model
    ```bash
    # For Example
    cd /path/to/init-i

    # Notice: no need to give extension here
    ./converter/yolo-converter.sh ./app/trt/yolov4-tiny/yolov4-tiny-416

    # After convert yolov4-tiny-416 should be generated.
    ls ./app/trt/yolov4-tiny/yolov4-tiny-416* | grep trt
    ./app/trt/yolov4-tiny/yolov4-tiny-416.trt
    ```
    * Convert performance
      * `1050 Ti`
        * yolo to onnx: 1s
        * onnx to tensorrt: 39s
4. Run demo.py
    ```
    cd /path/to/init-i
    python3 tensorrt_demo.py -c ./app/trt/yolov4-tiny/app.json
    ```