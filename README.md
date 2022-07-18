# iVIT-I For NVIDIA
iVIT-I for NVIDIA x86 platform

## Pre-requirements
* NVIDIA gpu driver ( 430+ )
* Install [docker](https://max-c.notion.site/Install-Docker-9a0927c9b8aa4455b66548843246152f) and [nvidia-docker2](https://max-c.notion.site/Install-NVIDIA-Docker-b15e1b2930f646f389675bde6a04c9e2)


## Prepare Environment

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
    ./docker/run.sh -i

    # Run with CLI mode
    ./docker/run.sh -ci
    ```

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


# For Developer
* init python api
    * Add a sample task
        > If we want to create a task called `test`
        
        1. create the folder name `test` and upload `model`, `label`, `task.json`, `model.json` on the cloud.
        2. change the permission to anyone and copy the download link.
        2. copy download script ( `custom_download.sh` ) from other task and modify the ID which could parse from download link.
    
    * Add an application
        > If we want to create an application called `tracking`
        
        1. define application module ( `tracking.py` ) in `./ivit_i/app/`.
        2. define the class object called `Tracking`, capitalizing the first word.
        3. inherit the module `App` in `ivit_i.app.common`.
        4. define custom parameter in `__init__()` and define the custom `__call__()` function.
        5. add judgment for new application like `if app_tag_in_config=="tracking"` in `handler.py`.
    
