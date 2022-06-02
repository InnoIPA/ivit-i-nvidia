# Mask detector which trained from `Darknet`

1. Enter the environment
    ```bash
    ./docker/run.sh -f nvidia -m
    ```
2. Download model
    ```bash
    ./app/mask_detection_yolo/download_model.sh
    ```
3. Convert Model
    ```bash
    # Notice: no need to give extension here
    ./converter/yolo-converter.sh ./app/mask_detection_yolo/yolov4-tiny-mask
    ```
4. Modify the application configuration `task.json`, `yolov4-tiny-mask.json`
    |   key             |   example     |   descr       |
    |   ---             |   ---         |   ---         |
    |   source      |   /dev/video0 |   the input data
    |   thres           |   0.5         |   the threshold of object detection

5. Run demo.py
    ```
    python3 demo.py -c ./app/mask_detection_yolo/task.json
    ```