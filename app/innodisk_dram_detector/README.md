# Yolov3-tiny: official yolov3-tiny model trained from `DarkNet`

1. Enter the environment
    ```bash
    ./docker/trt/run.sh -f trt -m
    ```
2. Download model
    ```shell
    # In the yolov3-tiny folder
    cd /path/to/init-i/app/trt/innodisk_dram_detector              # modify to your path
    ./download_model.sh

    # Prepare testing data
    ./download_testing_data.sh
    ```
3. Convert Model
    ```shell
    # For Example
    cd /path/to/init-i
    
    # Notice: no need to give extension here
    ./converter/yolo-converter.sh ./app/trt/innodisk_dram_detector/yolov3-tiny-dram    
    ```
4. Run the sample code via CLI
    ```bash
    # modify the input_data in app.json
    # ./app/trt/innodisk_dram_detector/innodisk_dram.avi
    python3 tensorrt_demo.py -c ./app/trt/innodisk_dram_detector/app.json
    ```
