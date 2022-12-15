![LOGO](docs/images/iVIT-I-Logo-B.png)

# iVIT-I For NVIDIA
iVIT-I for NVIDIA x86 platform

* [Pre-requirements](#pre-requirements)
* [Prepare Environment](#prepare-environment)
* [Run Samples](#run-samples)
* [Fast Testing](#fast-testing)
* [Web API](#web-api)

# Pre-requirements
* NVIDIA gpu driver ( 430+ )
* [Docker](https://max-c.notion.site/Install-Docker-9a0927c9b8aa4455b66548843246152f)
* [NVIDIA Container](https://max-c.notion.site/Install-NVIDIA-Docker-b15e1b2930f646f389675bde6a04c9e2)


# Prepare Environment

1. Clone Repository

    ```bash
    git clone https://github.com/InnoIPA/ivit-i-nvidia.git && cd ivit-i-nvidia
    ```

2. Run the docker container with web api


    * Run container with **web api**
        ```bash
        sudo ./docker/run.sh
        ```

    * Run container with **command line mode**
        ```bash
        sudo ./docker/run.sh -c
        ```

    * Run container without initialize sample
        ```bash
        sudo ./docker/run.sh -n -c

        # if you need to initialize samples
        ./init_samples.sh
        # if you need to launch web api
        ./exec_web_api.sh
        ```

    * Run docker container step by step for developer

        Here is the [documentation](docs/activate_env_for_developer.md) explaining the workflow of `run docker container`.

        
# Run Samples
* Please follow the `README.md` in each samples, the common workflow like below
    1. Enter docker container.
    2. Choose a sample.
    3. Download the model.
    4. Convert the model if needed.
    5. Using [demo.py](./demo.py) to run the sample.
        * For example: `python3 demo.py -c ${TASK}.json`
        * `-s` run without display, only console output.
        * `-r` run with RTSP ([`rtsp://localhost:8554/test`](rtsp://localhost:8554/test)) .

* More detail
    | name | describe 
    | ---- | -------- 
    | [classification-sample](task/classification-sample/README.md)    |  Classfication sample.  
    | [yolov3-tiny](task/yolov3-tiny-sample/README.md)   | The objected detection sample which trained from `Darknet`.
    | [yolov4-tiny](task/yolov4-tiny-sample/README.md)   | The objected detection sample which trained from `Darknet`.
    | [yolov4](task/yolov4-sample/README.md)   | The objected detection sample which trained from `Darknet`.
    | [wrong-side-detect](task/wrong-side-detect/README.md)   | The application sample of detecting moving direction.
    | [traffic-flow-detect](task/traffic-flow-detect/README.md)   | The application sample of tracking object.
    | [parking-lot-detect](task/parking-lot-detect/README.md)   | The application sample of detecting object is in area or not.

# Fast Testing
We provide the fast-test for each sample, please check [here](./test/README.md).

# Web API
<details>
    <summary>
        We recommand <a href="https://www.postman.com/">Postman</a> to test your web api , you could see more detail in <code>{IP Address}:{PORT}/apidocs</code>.
    </summary>
    <img src="docs/images/apidocs.png" width=80%>
    
</details>
<br>

# Credit
* Using [aler9/rtsp-simple-server](https://github.com/aler9/rtsp-simple-server) to handle RTSP stream.
* Convert to WebRTC by using [deepch/RTSPtoWeb](https://github.com/deepch/RTSPtoWeb).
* Convert TensorRT egnine from darknet referring from [jkjung-avt/tensorrt_demos](https://github.com/jkjung-avt/tensorrt_demos)