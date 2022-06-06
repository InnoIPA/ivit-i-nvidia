# iNIT-I For NVIDIA
iNIT-I for NVIDIA x86 platform

## Pre-requirements
* NVIDIA gpu driver ( 430+ )
* Install [docker](https://max-c.notion.site/Install-Docker-9a0927c9b8aa4455b66548843246152f) and [nvidia-docker2](https://max-c.notion.site/Install-NVIDIA-Docker-b15e1b2930f646f389675bde6a04c9e2)
* Clone Repository
    ```bash
    # clone repo and submodule
    git clone --recurse-submodules https://github.com/MaxChangInnodisk/init-i-nvidia.git
    
    # check if submodule is downloaded
    ls ./init_i/web
    ai  api  app.py  __init__.py  __pycache__  utils

    # if not exist then download submodule again
    git submodule init && git submodule update
    ```

## Build Environment

1. Build the docker images
    ```bash
    ./docker/build.sh

    Build the docker image. (init-i/nvidia:v0.1)
    Sending build context to Docker daemon  16.38kB
    Step 1/6 : FROM nvcr.io/nvidia/tensorrt:21.03-py3
    ---> 0371e1584b77
    Step 2/6 : WORKDIR /workspace
    ---> Using cache
    ---> 19f7e2604451
    Step 3/6 : COPY ["./format_print.sh", "./requirements.sh", "./patch_pose.sh", "/workspace/" ]
    ---> Using cache
    ---> a2fb682729b8
    Step 4/6 : ENV DEBIAN_FRONTEND noninteractive
    ---> Using cache
    ---> 2ece577d91eb
    Step 5/6 : RUN chmod +x ./requirements.sh && ./requirements.sh && chmod +x ./patch_pose.sh && ./patch_pose.sh && rm ./*.sh
    ---> Using cache
    ---> 07f638af5065
    Step 6/6 : ENTRYPOINT [ "/bin/bash", "-c" ]
    ---> Using cache
    ---> 2290a33efdc1
    Successfully built 2290a33efdc1
    Successfully tagged init-i/nvidia:v0.1
    ```
    > about 12 min.
2. Run the docker container
    ```shelld
    ./docker/run.sh -f nvidia -v v0.1 -m
    ```

## Samples
| name | describe 
| ---- | -------- 
| [classification_sample](app/classification_sample/README.md)    |  Classfication sample.  
| [usb_detector](app/usb_detector/README.md)   | The objected detection sample which trained from NVIDIA TAO Toolkit.
| [people_seg_sample](app/people_seg_sample/README.md)   | Peopple segmentation for the `etlt` model download from NVIDIA NGC.
| [humanpose_sample](app/humanpose_sample/README.md) | Human pose estimation which base on [trt_pose](https://github.com/NVIDIA-AI-IOT/trt_pose)


# Developer
* Add submodule
    ```bash
    git submodule add --name web https://github.com/MaxChangInnodisk/init-i-web-api.git ./init_i/web
    ```