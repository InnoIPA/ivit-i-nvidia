# Moving-Direction-Sample: 

1. Enter the environment
    ```bash
    ./docker/run.sh -c
    ```
2. Download model
    ```bash 
    # Download Model
    cd /workspace/
    python3 ./task/moving-direction-sample/custom_download.py -m yolov4-tiny -s 416 -f ./task/model

    # Download Data
    ./task/moving-direction-sample/download_data.sh
    ```
3. Convert Model
    ```bash
    
    # Convert model
    cd /workspace
    ./converter/yolo-converter.sh   ./model/yolov4-tiny/yolov4-tiny-416

    # After convert yolov4-tiny-416 should be generated.
    ls ./model/yolov4-tiny | grep trt

    ```
    * Convert performance
      * `1050 Ti`
        * yolo to onnx: 1s
        * onnx to tensorrt: 39s

4. Run demo.py
    ```
    cd /workspace
    python3 demo.py -c ./task/yolov4-tiny/task.json
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