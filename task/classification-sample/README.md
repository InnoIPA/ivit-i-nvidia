# TAO-Classification for iVIT-TensorRT
Classification model which trained from NVIDIA TAO or iTAO.

## Enter the iVIT-I container
    ```bash
    cd </path/to/iVIT-I>
    sudo ./docker/run.sh -nc
    ```

## For Sample Onnx Model

1. Download Sample Model ( ONNX )
    ```bash
    # download data
    ./task/classification-sample/download_data.sh

    # download model - resnet34
    ./task/classification-sample/download_model.sh
    ```
    * Reference from [ONNX Model Zoo](https://github.com/onnx/models/tree/main/vision/classification/resnet)

2. Convert Model
    ```bash
    trtexec \
    --onnx=/workspace/model/resnet/resnet34.onnx \
    --batch=1 \
    --saveEngine=/workspace/model/resnet/resnet34.trt
    ```
    * GTX 1050Ti Convert ResNet34 Cost: About 30 sec.

3. Prepare the application configuration `task.json`
    
    > Notice: 
    > if you only want to run with `tensorrt_demo.py`, you could ignore the option below: `category`, `application`, `name`, `source_type`.

    ```json
    {
        "framework": "tensorrt",
        "source": "/dev/video2",
        "prim": {
            "model_json": "./app/classification-sample/classification.json"
        },
        "category": "sample",
        "application": {
            "name": "default"
        },
        "name": "classification-sample",
        "source_type": "V4L2"
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

4. Prepare the model configuration
    ```json
    {
        "tag": "cls",
        "tensorrt": {
            "model_path": "./task/classification-sample/resnet50.engine",
            "label_path": "./task/classification-sample/imagenet.txt",
            "device": "NVIDIA GeForce GTX 1050 Ti",
            "input_size": "3,224,224",
            "preprocess": "caffe",
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
4. Run demo
    ```
    python3 demo.py -c task/classification-sample/task.json
    ```
