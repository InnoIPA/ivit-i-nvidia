# Human Pose Estimation for iVINNO-TensorRT

## Pre-requirements
0. Enter the container
```bash
sudo ./docker/run.sh -m
```

1. Download Model

   * run the script
       ```bash
        cd /path/to/iVIT-I
        ./task/humanpose_sample/download_model.sh
       ```
   * choose the model
       ```
       /****************************************************************************************************/
       /*                                                                                                  */
       /*    Index   Name                                 Jetson Nano   Jetson Xavier   Weights            */
       /*    1       resnet18_baseline_att_224x224_A      22            251             download (81MB)    */
       /*    2       densenet121_baseline_att_256x256_B   12            101             download (84MB)    */
       /*                                                                                                  */
       /****************************************************************************************************/
       Please enter the index you want to download [<idx>/all] : 
       ```

2. Convert Model

    Use pose-converter to generate tensorrt engine from pytorch mdoel.
    
    ```bash
    # For Example

    ./converter/pose-converter \
    -m ./task/humanpose_sample/resnet18_baseline_att_224x224_A.pth \
    -j ./task/humanpose_sample/label.json \
    -e ./task/humanpose_sample/resnet18_baseline_att_224x224_A.engine

    ###############################
    # get human pose parser ... 0.002 s 
    # Downloading: ... 7.113 s 
    # do convert ... 
    # convert model ( 97.603s )
    ```

    | argument | describe |
    | ---- | ----- |
    | `-m` | the input of the model
    | `-j` | label file for parse the model 
    | `-e` | the output path of the tensorrt engine

3. Prepare the application configuration `task.json`
    
    > Notice: 
    > if you only want to run with `demo.py`, you could ignore the option below: `category`, `application`, `name`, `source_type`.

    ```json
    {
        "framework": "tensorrt",
        "source": "./data/web/production_ID_4806533.mp4",
        "prim": {
            "model_json": "./app/humanpose_sample/humanpose.json"
        },
        "category": "sample",
        "application": "human pose",
        "name": "humanpose_sample",
        "source_type": "Video"
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
        "tag": "pose",
        "tensorrt": {
            "model_path": "./app/humanpose_sample/resnet18_baseline_att_224x224_A.engine",
            "label_path": "./app/humanpose_sample/label.json",
            "device": "NVIDIA GeForce GTX 1050 Ti",
            "input_size": "3,224,224",
            "preprocess": "torch",
            "thres": "0.7"
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
python3 demo.py -c task/humanpose_sample/task.json
```

---

# For Developer

## Reference
1. Human Pose Estimation in iVINNO base on [NVIDIA-AI-IOT_pose](https://github.com/NVIDIA-AI-IOT_pose) 
2. We provide a prue repository of trt_pose for ivinno. [p513817/pure_trt_pose](https://github.com/p513817/pure_trt_pose)

## Pre-processing
> Classic Torch mode
1. Convert to RGB format.
2. Rescale to the target size via `cv2.resize`.
3. Scale pixels between 0 and 1.
4. Normalize each channel with respect to the ImageNet dataset.
    * RGB Average = [0.485, 0.456, 0.406] 
    * Standard Deviation = [0.229, 0.224, 0.225]

## Post-processing
1. Two results (`cmap` and `paf`) will be generated after fnference.
2. The shape of them should to resized to `[1, 18, input_size//4, intput_size//4]`
3. Three objects (`counts`, `objects`, `peaks`) will be parsed via `ParseObjects`
4. Draw the image with `DrawObjects`