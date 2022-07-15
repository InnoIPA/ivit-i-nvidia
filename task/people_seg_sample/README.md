# People Instance Segmentation for iVIT-TensorRT
You can download PeopleSegNet model from [NGC](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/peoplesegnet/files).

## Pre-requirements
0. Enter the container
    ```bash
    sudo ./docker/run.sh -m
    ```
1. Download Model
    ```bash 
    ./task/people_seg_sample/download_data.sh
    ./task/people_seg_sample/download_model.sh

    # After downloaded
    tree ./task/people_seg_sample
    .
    |-- README.md
    |-- task.json
    |-- download_model.sh
    |-- people_seg.json
    |-- peoplesegnet.txt
    |-- peoplesegnet_resnet50.etlt
    `-- peoplesegnet_resnet50_int8.txt
    ```

2. Convert Model

    Use pose-converter to generate tensorrt engine from pytorch mdoel.
    ```bash
    cd /path/to/iNIT-I

    # Float 32
    ./converter/tao-converter -k nvidia_tlt \
    -d 3,576,960 \
    -o mask_fcn_logits/Conv2D,mask_fcn_logits/BiasAdd \
    -e /workspace/task/people_seg_sample/peoplesegnet.engine \
    -t fp32 \
    -i nchw \
    -m 1 \
    /workspace/task/people_seg_sample/peoplesegnet_resnet50.etlt

    # Int 8
    ./converter/tao-converter -k nvidia_tlt \
    -d 3,576,960 \
    -o mask_fcn_logits/Conv2D,mask_fcn_logits/BiasAdd \
    -c /workspace/task/people_seg_sample/peoplesegnet_resnet50_int8.txt \
    -e /workspace/task/people_seg_sample/peoplesegnet_int8.engine \
    -t int8 \
    -i nchw \
    -m 1 \
    /workspace/task/people_seg_sample/peoplesegnet_resnet50.etlt
    ```

    * The convert time with my graphic card ( NVIDIA Tesla A2 )
        |   Precision       |   Time   
        |   ---             |   ---
        |   FP16            |   2 minutes
        |   INT8            |   08->

3. Create a label file for inference
    ```bash
    cat /workspace/task/people_seg_sample/peoplesegnet.txt

    other
    people
    ```

4. Prepare the application configuration `task.json`
    
    > Notice: 
    > if you only want to run with `tensorrt_demo.py`, you could ignore the option below: `category`, `application`, `name`, `source_type`.

    ```json
    {
        "framework": "tensorrt",
        "source": "rtsp://admin:admin@172.16.21.1:554/snl/live/1/1/n",
        "prim": {
            "model_json": "./app/people_seg_sample/people_seg.json"
        },
        "category": "sample",
        "application": "people track",
        "name": "people_seg_sample",
        "source_type": "RTSP"
    }
    ```
    |   item        |   describe   
    |   ---         |   ----        
    |   framework   |   [ "tensorrt", "openvino" ]
    |   source  |   [ v4l2, image path , video path, RTSP url ]
    |   prim        |   the path to model configuration
    |   category    |   the category of this application
    |   application |   the sub category of this applicathtion
    |   name    |   the name of this application
    |   source_type  |   the type of input data [ "V4L2", "Image", "Video", "RTSP" ]

5. Prepare the model configuration
    ```json
    {
        "tag": "seg",
        "tensorrt": {
            "model_path": "./app/people_seg_sample/peoplesegnet.engine",
            "label_path": "./app/people_seg_sample/peoplesegnet.txt",
            "device": "NVIDIA GeForce GTX 1050 Ti",
            "input_size": "3,576,960",
            "preprocess": "torch",
            "thres": "0.9"
        }
    }
    ```
    |   item        |   describe   
    |   ---         |   ----        
    |   tag         |   the task with abbr name of the AI model, e.g.[ "cls", "obj", "pose", "seg" ]
    |   { af }      |   the framework for double check, e.g.[ "tensorrt", "openvino" ]
    |   model_path  |   the path to model
    |   label_path  |   the path to label
    |   device      |   the GPU device with full name, you could check `Product Name` with `nvidia-smi -q | less`
    |   input_size  |   the input size of the AI model
    |   preprocess  |   the process mode in [ 'torch', 'caffe' ]
    |   thres       |   the threshold


## Run Human Pose Estimation Sample

``` 
python3 demo.py -c task/people_seg_sample/task.json
```

---

# For Developer
