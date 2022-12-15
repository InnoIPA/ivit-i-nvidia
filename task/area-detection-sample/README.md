# Area-Detection-Sample
> custom yolov4 model trained from `DarkNet`

1. Enter the environment
    ```bash
    sudo ./docker/run.sh -c -n
    ```
2. Define Parameters
    ```bash
    TASK=area-detection-sample
    MODEL=yolov4-tiny
    SIZE=416
    DIR=/workspace/model/${MODEL}

    # Double Check
    echo -e "\n* ${TASK}\n* ${MODEL}\n* ${SIZE}\n* ${DIR} \n" 
    ```
2. Download model and data
    ```bash
    cd /workspace/

    # Model
    python3 ./task/${TASK}/custom_download.py \
    -m ${MODEL} -s ${SIZE} -f ${DIR}

    # Data
    ./task/${TASK}/download_data.sh
    ```
3. Convert Model
    ```bash
    cd /workspace
    ./converter/yolo-converter.sh "${DIR}/${MODEL}-${SIZE}"
    ```
    * Convert performance
      * `1050 Ti`
        * yolo to onnx: 1s
        * onnx to tensorrt: 39s
4. Run demo.py
    ```
    cd /workspace
    python3 demo.py -c ./task/${TASK}/task.json
    ```

5. More Options
    ```bash
    python3 demo.py -h

    Output <<EOF
    usage: demo.py [-h] [-c CONFIG] [-s] [-r] [-d] [-m MODE] [-i IP] [-p PORT] [-n NAME]
    
    optional arguments:
    -h, --help            show this help message and exit
    -c CONFIG, --config CONFIG
                            The path of application config
    -s, --server          Server mode, not to display the opencv windows
    -r, --rtsp            RTSP mode, not to display the opencv windows
    -d, --debug           Debug mode
    -m MODE, --mode MODE  Select sync mode or async mode{ 0: sync, 1: async }
    -i IP, --ip IP        The ip address of RTSP uri
    -p PORT, --port PORT  The port number of RTSP uri
    -n NAME, --name NAME  The name of RTSP uri
    EOF
    
    ```