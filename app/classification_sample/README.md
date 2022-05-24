# TAO-Classification for iVINNO-TensorRT
Classification model which trained from NVIDIA TAO or iTAO.

## Enter the iNIT-I container
    ```bash
    cd /path/to/iNIT-I
    # for desktop user
    sudo ./docker/trt/run.sh -f trt -m
    # for server user
    sudo ./docker/trt/run.sh -f trt -m
    ```
    * `-m` means magic,print information with funny format.

## For Sample Torch Model
1. Download Sample Model ( Torch )
    ```bash
    cd app/trt/classification_sample
    python3 download_resnext50.py

    # ------------------------------------
    # My situation
    # Download ResNeXt50 ... 21.674s
    # Convert to TensorRT ... 28.976s
    # Save the tensorrt engine ... 0.615s
    ```
2. Prepare the application configuration `app.json`
    
    > Notice: 
    > if you only want to run with `tensorrt_demo.py`, you could ignore the option below: `category`, `application`, `app_name`, `input_type`.

    ```json
    {
        "framework": "tensorrt",
        "input_data": "/dev/video2",
        "prim": {
            "model_json": "./app/trt/classification_sample/classification.json"
        },
        "category": "sample",
        "application": "classification",
        "app_name": "classification_sample",
        "input_type": "V4L2"
    }
    ```
    |   item        |   describe   
    |   ---         |   ----        
    |   framework   |   [ "tensorrt", "openvino" ]
    |   input_data  |   [ v4l2, image path , video path, RTSP url ]
    |   prim        |   the path to model configuration
    |   category    |   the category of this application
    |   application |   the sub category of this applicathtion
    |   app_name    |   the name of this application
    |   input_type  |   the type of input data [ "V4L2", "Image", "Video", "RTSP" ]

3. Prepare the model configuration
    ```json
    {
        "tag": "cls",
        "tensorrt": {
            "model_path": "./app/trt/classification_sample/resnet50.engine",
            "label_path": "./app/trt/classification_sample/imagenet.txt",
            "device": "NVIDIA GeForce GTX 1050 Ti",
            "input_size": "3,224,224",
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

## For TAO Classification Model
1. Prepare Model and Label
    ```shell
    tree
    .
    |-- README.md
    |-- mask_classifier.txt # label file
    `-- model.etlt          # etlt model
    ```
2. Convert Model
    ```shell
    # For Example: mask_classifier is a classification model can detect mask and non-mask.
    $ cd /ivinno-trt

    $ ./converter/tao-converter \
    -k nvidia_tlt \
    -o predictions/Softmax \
    -d 3,224,224 \
    -i nchw \
    -m 1 -t fp32 \
    -e /ivinno-trt/models/TAO-Classification/mask_clssifier.trt \
    -w 1610612736 \
    /ivinno-trt/models/TAO-Classification/model.etlt

    # [INFO] Detected 1 inputs and 1 output network tensors.
    ```
3. Create label file `/ivinno-trt/models/TAO-Classfication/mask_classifier.txt`
    ```
    mask
    non-mask
    ```
4. Update informations about model and label in `/ivinno-trt/config/trt/model_config/classification.json`
    ```
    model_path=<path/to/engine>
    label_path=<path/to/label>
    ```
5. Run tensorrt_demo.py
    ```
    $ python3 tensorrt_demo.py -c app/trt/classification_sample/app.json
    ```
---

# For Developer ( TAO )

## Reference
1. The model in classification_sample should be trained from NVIDIA TAO or iTAO and must be the .

## Pre-processing
* Classic Caffe mode
  1. Convert the images from RGB to BGR.
  2. Rescale to the target size via `cv2.resize`.
  3. zero-center each color channel with respect to the ImageNet dataset.
      * BGR -> [103.939, 116.779, 123.68]

## Post-processing
1. Four objects ( detections, bounding boxes, socres, classes ) in results.
2. Bounding Boxes have to reshape to [-1, 4].
3. You can parse out four positions ( top_left, top_right, bottom_letf, bottom_right ) in each bounding box.