# Fast Testing
Fast Testing for `NVIDIA` platform:
1. Download data and model from Google Drive.
2. Build the library if the model is from darknet.
3. Convert to TensorRT Engine.
4. Run demo script if you give the argument `-r`, you could use `-r` to disable the cv window.

* Run the testing script
    ```bash
    ./docker/run.sh -c
    <script.sh> < -r > < -s > < -h >
    ```
    |   name    |   descr                   
    |   ----    |   -----
    |   `-r`    |   run the demo script and display the result
    |   `-s`    |   server mode, only print the result not dispay
    |   `-h`    |   show help information

* Run script outside the docker container

    ```bash
    docker start ivit-i-nvidia
    docker exec -it ivit-i-nvidia <script.sh> < -r > < -s > < -h >
    ```

* Examples
    * classification.sh
        ```bash
        docker exec -it ivit-i-nvidia ./test/classification.sh -r
        ```
    * ngc_people_seg.sh
        ```bash
        docker exec -it ivit-i-nvidia ./test/ngc_people_seg.sh -r
        ```
    * pose_estimation.sh
        ```bash
        docker exec -it ivit-i-nvidia ./test/pose_estimation.sh -r
        ```
    * innodisk_dram_detection.sh
        ```bash
        docker exec -it ivit-i-nvidia ./test/innodisk_dram_detection.sh -r
        ```
    * yolov3-tiny.sh
        ```bash
        docker exec -it ivit-i-nvidia ./test/yolov3-tiny.sh -r
        ```
    * yolov4-tiny.sh
        ```bash
        docker exec -it ivit-i-nvidia ./test/yolov4-tiny.sh -r
        ```
    * yolov4.sh
        ```bash
        docker exec -it ivit-i-nvidia ./test/yolov4.sh -r
        ```