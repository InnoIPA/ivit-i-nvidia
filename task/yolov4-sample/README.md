# Yolov4-tiny: official yolov4 model trained from `DarkNet`

1. Enter the environment
    ```bash
    ./docker/run.sh -c
    ```
2. Download model
    ```bash
    # In the yolov4 folder
    cd /path/to/ivit-i/task/yolov4              # modify to your path
    python3 custom_download.py -m yolov4 -s 416 

    # In the ivit-i folder
    python3 ./task/yolov4-sample/custom_download.py -m yolov4 -s 416 -f ./task/yolov4-sample
    
    # Download Data
    ./task/yolov3-tiny-sample/download_data.sh
    ```
3. Convert Model
    ```bash
    # For Example
    cd /path/to/ivit-i

    # Notice: no need to give extension here
    ./converter/yolo-converter.sh ./model/yolov4/yolov4-416

    # After convert yolov4-416 should be generated.
    ls ./model/yolov4/yolov4-416* | grep trt
    
    ```
    * Convert performance
      * `1050 Ti`
        * yolo to onnx: 8s
        * onnx to tensorrt: 1m 51s ( 111s )
4. Run demo.py
    ```
    cd /path/to/ivit-i
    python3 demo.py -c ./task/yolov4-sample/task.json
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