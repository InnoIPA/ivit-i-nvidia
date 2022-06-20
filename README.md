# iNIT-I For NVIDIA
iNIT-I for NVIDIA x86 platform

## Pre-requirements
* NVIDIA gpu driver ( 430+ )
* Install [docker](https://max-c.notion.site/Install-Docker-9a0927c9b8aa4455b66548843246152f) and [nvidia-docker2](https://max-c.notion.site/Install-NVIDIA-Docker-b15e1b2930f646f389675bde6a04c9e2)


## Prepare Environment

1. Clone Repository and submodule
    > submodule is web api which will be place in [init_i/web](./init_i/web)
    ```bash
    # clone repo and submodule
    git clone --recurse-submodules https://github.com/MaxChangInnodisk/init-i-nvidia.git
    
    # check if submodule is downloaded
    ls ./init_i/web
    ai  api  app.py  __init__.py  utils

    # if not exist then download submodule again
    # $ git submodule init && git submodule update
    ```

2. Build the docker images
    ```bash
    ./docker/build.sh

    Build the docker image. (init-i/nvidia:v0.1)
    Sending build context to Docker daemon  16.38kB
    Step 1/6 : FROM nvcr.io/nvidia/tensorrt:21.03-py3
    ---> 0371e1584b77
    # ...
    Successfully built 2290a33efdc1
    Successfully tagged init-i/nvidia:v0.1
    ```
    > about 12 min.
3. Run the docker container with web api
    ```bash
    ./docker/run.sh -f nvidia -v v0.1 -wm
    # enter container without web api
    ./docker/run.sh -f nvidia -v v0.1 -m
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
    | [classification_sample](app/classification_sample/README.md)    |  Classfication sample.  
    | [usb_detector](app/usb_detector/README.md)   | The objected detection sample which trained from NVIDIA TAO Toolkit.
    | [people_seg_sample](app/people_seg_sample/README.md)   | Peopple segmentation for the `etlt` model download from NVIDIA NGC.
    | [humanpose_sample](app/humanpose_sample/README.md) | Human pose estimation which base on [trt_pose](https://github.com/NVIDIA-AI-IOT/trt_pose)


# For Developer
* init python api
    * Add a sample task
        > If we want to create a task called `test`
        
        1. create the folder name `test` and upload `model`, `label`, `task.json`, `model.json` on the cloud.
        2. change the permission to anyone and copy the download link.
        2. copy download script ( `custom_download.sh` ) from other task and modify the ID which could parse from download link.
    
    * Add an application
        > If we want to create an application called `tracking`
        
        1. define application module ( `tracking.py` ) in `./init_i/app/`.
        2. define the class object called `Tracking`, capitalizing the first word.
        3. inherit the module `App` in `init_i.app.common`.
        4. define custom parameter in `__init__()` and define the custom `__call__()` function.
        5. add judgment for new application like `if app_tag_in_config=="tracking"` in `handler.py`.
    