# Yolov3-tiny: official yolov3-tiny model trained from `DarkNet`

1. Enter the environment
    ```bash
    sudo ./docker/run.sh -m
    ```
2. Download model
    ```shell
    ./task/innodisk_dram_detector/download_model.sh

    # Prepare testing data
    ./task/innodisk_dram_detector/download_testing_data.sh
    ```
3. Convert Model
    ```shell
    # Notice: no need to give extension here
    ./converter/yolo-converter.sh ./task/innodisk_dram_detector/yolov3-tiny-dram    
    ```
4. Run the sample code via CLI
    ```bash
    # modify the source in task.json
    # ./task/innodisk_dram_detector/innodisk_dram.avi
    python3 demo.py -c ./task/innodisk_dram_detector/task.json
    ```
