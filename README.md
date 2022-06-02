# iNIT-I For NVIDIA
Introduce of iNIT-I-NVIDIA

## Pre-requirements
* NVIDIA gpu driver ( 430+ )
* Install [docker](https://max-c.notion.site/Install-Docker-9a0927c9b8aa4455b66548843246152f) and [nvidia-docker2](https://max-c.notion.site/Install-NVIDIA-Docker-b15e1b2930f646f389675bde6a04c9e2)

## Build Environment

### Docker
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
    about 12 min.
2. Run the docker container
    ```shelld

    .docker/trt/run.sh                  # run without camera, the name will be "ivinno-trt"
    .docker/trt/run.sh /dev/video0      # run with camera, the container name will be "ivinno-trt-cam"
    ./docker/trt/run.sh /dev/video0 1   # run with camera and mount gpu ( id:1 )
    ```
## Samples
| name | describe 
| ---- | -------- 
| [classification_sample](app/trt/classification_sample/README.md)    |  Classfication sample for NVIDIA TAO Toolkit.  
| [innodisk_sample](app/trt/usb_detector/README.md)   | YOLOv4 sample for NVIDIA TAO Toolkit.
| [people_seg_sample](app/trt/people_seg_sample/README.md)   | Peopple segmentation for the `etlt` model download from NVIDIA NGC.
| [humanpose_sample](app/trt/humanpose_sample/README.md) | Human pose estimation which base on [trt_pose](https://github.com/NVIDIA-AI-IOT/trt_pose)

# Overview

```shell
.                                       # ---------------------------------------------------------
├── config                              # CONFIGURATIONS
│   └── trt                                 
│       ├── app_config                      # app config which could run with demo.py, app config have to cooperate with model config
│       │   ├── classification.json
│       │   ├── human_pose.json
│       │   ├── people_seg.json
│       │   └── yolov4.json
│       └── model_config                    # place all configs of model, user could adjust the parameters of the model .
│           ├── classification.json
│           ├── humanpose.json
│           ├── people_segmentation.json
│           └── yolov4.json
|                                       # ---------------------------------------------------------
├── converter                           # CONVERTER
│   ├── pose-converter                      # converter human pose model from torch to tensorrt engine.
│   └── tao-converter                       # converter for TAO ( etlt model )
|                                       # ---------------------------------------------------------
├── docker                              # ENVIRONMENT
│   └── trt                                 # environment for tensorrt 
│       ├── build.sh                            # build the docker image via Dockerfile.
│       ├── Dockerfile                          # the building workflow.
│       ├── format_print.sh                     # some printing utility.
│       ├── patch_pose.sh                       # the pre-requirement for human pose estimation.
│       ├── requirements.sh                     # requirement for environment.
│       └── run.sh                              # run the docker container.
|
|                                       # ---------------------------------------------------------
├── ivinno                              # API
│   └── trt                                 # ivinno api for tensorrt
|
|                                       # ---------------------------------------------------------
├── models                              # SAMPLES
│   ├── HumanPose                           # Human Pose Estimation
│   │   ├── download_model.sh                   # download human pose model 
│   │   ├── human_pose.json                     # provide the default label
│   │   └── README.md
│   ├── PeopleSegNet                        # People Segmentation 
│   │   ├── download_model.sh                   # download PeopleSegNet from NVIDIA NGC
│   │   └── README.md                           # provide the default label
│   ├── TAO-Classification                  # Classification for the model trained from TAO  
│   │   └── README.md
│   └── TAO-YOLOv4                          # YOLOv4 for the model trained from TAO
│       └── README.md
├── README-TRT.md
└── tensorrt_demo.py

```


# Overview of API
```shell
./ivinno/trt
|         
|-- common                      # utilities for TensorRT
|   |-- api.py                  # return the target api
|   |-- common.py               # any basic tensorrt function in here, also include the parents of each model's api.
|   `-- process.py              # include pre-process and post-process
|
|-- utils                       # utilities for Other
|   |-- drawing_tools.py        # draw the image base on the results.
|   |-- logger.py               # config the logger.
|   |-- parser.py               # the parse tools like 'load_json', 'load_txt', etc.
|   `-- timer.py                # custom timer to calculate running time.
|
|-- cls                     
|   `-- classification.py       # classification
|-- obj
|   `-- yolov4.py               # yolov4
|-- pose
|   `-- bodypose.py             # human pose estimation
`-- seg
    `-- segmentation.py         # instance segmentation
```

# Developer for web api
```bash
git submodule add --name web https://github.com/MaxChangInnodisk/init-i-web-api.git ./init_i/web

```