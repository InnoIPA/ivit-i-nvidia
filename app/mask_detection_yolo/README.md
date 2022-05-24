# Mask detector which trained from `Darknet`

1. Enter the environment
    ```bash
    ./docker/trt/run.sh -f trt -m
    ```
2. Download model
    ```bash
    cd ./app/trt/mask_detection_yolo
    ./download_model.sh
    ```
3. Convert Model
    ```bash
    # For Example
    cd /path/to/init-i

    # Notice: no need to give extension here
    ./converter/yolo-converter.sh ./app/trt/mask_detection_yolo/yolov4-tiny-mask
    ```
4. Modify the application configuration `app.json`, `yolov4-tiny-mask.json`
    |   key             |   example     |   descr       |
    |   ---             |   ---         |   ---         |
    |   input_data      |   /dev/video0 |   the input data
    |   thres           |   0.5         |   the threshold of object detection

5. Run demo.py
    ```
    cd /path/to/init-i
    python3 tensorrt_demo.py -c ./app/trt/mask_detection_yolo/app.json
    ```