# Yolov3-tiny: official yolov3-tiny model trained from `DarkNet`

1. Enter the environment
    ```bash
    ./docker/run.sh -f nvidia -m
    ```
2. Download model
    ```shell
    ./app/innodisk_dram_detector/download_model.sh

    # Prepare testing data
    ./app/innodisk_dram_detector/download_testing_data.sh
    ```
3. Convert Model
    ```shell
    # Notice: no need to give extension here
    ./converter/yolo-converter.sh ./app/innodisk_dram_detector/yolov3-tiny-dram    
    ```
4. Run the sample code via CLI
    ```bash
    # modify the source in task.json
    # ./app/innodisk_dram_detector/innodisk_dram.avi
    python3 demo.py -c ./app/innodisk_dram_detector/task.json
    ```
