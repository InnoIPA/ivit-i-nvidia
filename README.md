# iVIT-I For NVIDIA
iVIT-I for NVIDIA x86 platform

* [Pre-requirements](#pre-requirements)
* [Prepare Environment](#prepare-environment)
* [Run Samples](#run-samples)
* [Web API](#web-api)
* [Fast Testing](#fast-testing)

# Pre-requirements
* NVIDIA gpu driver ( 430+ )
* Install [docker](https://max-c.notion.site/Install-Docker-9a0927c9b8aa4455b66548843246152f) and [nvidia-docker2](https://max-c.notion.site/Install-NVIDIA-Docker-b15e1b2930f646f389675bde6a04c9e2)


# Prepare Environment

1. Clone Repository and submodule
    > submodule is web api which will be place in [ivit_i/web](./ivit_i/web)
    ```bash
    # clone repo and submodule
    git clone --recurse-submodules https://github.com/InnoIPA/ivit-i-nvidia.git && cd ivit-i-nvidia
    
    # check if submodule is downloaded
    ls ./ivit_i/web
    ai  api  app.py  __init__.py  utils

    # if not exist then download submodule again
    # $ git submodule init && git submodule update
    ```

2. Build the docker images
    We use [ivit-i.json](ivit-i.json) to manage environment, like "docker image name", "docker image version", "port number", etc. You can see more detail in [setup_environment.md](docs/setup_environment.md)
    ```bash
    sudo ./docker/build.sh
    ```
    > about 12 min.

3. Run the docker container with web api
    ```bash
    # Initialize default sample
    sudo ./docker/run.sh

    # Run with CLI mode
    sudo ./docker/run.sh -c
    ```
    * To see more detail -> [running_workflow.md](docs/running_workflow.md)
        <img src="docs/images/run_script_info.png" width=80%>

# Run Samples
* Please follow the README.md in each samples, the common workflow like below:
    1. Choose a sample.
    2. Download model.
    3. Convert model if needed.
    4. Using [demo.py](./demo.py) to run the sample.
* Samples:
    | name | describe 
    | ---- | -------- 
    | [classification_sample](task/classification_sample/README.md)    |  Classfication sample.  
    | [yolov3-tiny](task/yolov3-tiny-sample/README.md)   | The objected detection sample which trained from NVIDIA TAO Toolkit.
    | [yolov4-tiny](task/yolov4-tiny-sample/README.md)   | The objected detection sample which trained from NVIDIA TAO Toolkit.
    | [yolov4](task/yolov4-sample/README.md)   | The objected detection sample which trained from NVIDIA TAO Toolkit.
    | [people_seg_sample](task/people_seg_sample/README.md)   | Peopple segmentation for the `etlt` model download from NVIDIA NGC.
    | [humanpose_sample](task/humanpose_sample/README.md) | Human pose estimation which base on [trt_pose](https://github.com/NVIDIA-AI-IOT_pose)

# Web API
<details>
    <summary>
        We recommand <a href="https://www.postman.com/">Postman</a> to test your web api , you could see more detail in <code>{IP Address}:{PORT}/apidocs</code>.
    </summary>
    <img src="docs/images/apidocs.png" width=80%>
</details>
<br>

# Fast Testing
We provide the fast-test for each sample, please check the [document](./test/README.md).