# TAO-Classification for iVIT-TensorRT
Classification model which trained from NVIDIA TAO or iTAO.

## Enter the iVIT-I container
    ```bash
    cd /path/to/iVIT-I
    # for desktop user
    ./docker/run.sh -c
    ```

## For Sample Torch Model
1. Download Sample Model ( Torch )
    ```bash
    # download data
    ./task/classification-sample/download_data.sh

    # download model
    python3 ./task/classification-sample/download_resnext50.py

    # ------------------------------------
    # My situation
    # Download ResNeXt50 ... 21.674s
    # Convert to TensorRT ... 28.976s
    # Save the tensorrt engine ... 0.615s
    ```
2. Prepare the application configuration `task.json`
    
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

3. Prepare the model configuration
    ```json
    {
        "tag": "cls",
        "tensorrt": {
            "model_path": "./task/classification-sample/resnet50.engine",
            "label_path": "./task/classification-sample/imagenet.txt",
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
4. Run demo
    ```
    python3 demo.py -c task/classification-sample/task.json
    ```

---

## For TAO Classification Model ( Archived )
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
    -e /path/to/mask_clssifier.trt \
    -w 1610612736 \
    /path/to/model.etlt

    # [INFO] Detected 1 inputs and 1 output network tensors.
    ```
3. Create label file `/ivinno-trt/models/TAO-Classfication/mask_classifier.txt`
    ```
    mask
    non-mask
    ```
4. Update informations about model and label in `task/classification-sample/task.json`
    ```
    model_path=<path/to/engine>
    label_path=<path/to/label>
    ```
5. Run tensorrt_demo.py
    ```
    $ python3 tensorrt_demo.py -c task/classification-sample/task.json
    ```

## For Developer ( TAO )

### Reference
* The model in classification-sample should be trained from NVIDIA TAO or iTAO and must be the .

### Pre-processing
* Classic Caffe mode
  1. Convert the images from RGB to BGR.
  2. Rescale to the target size via `cv2.resize`.
  3. zero-center each color channel with respect to the ImageNet dataset.
      * BGR -> [103.939, 116.779, 123.68]

### Post-processing
1. Four objects ( detections, bounding boxes, socres, classes ) in results.
2. Bounding Boxes have to reshape to [-1, 4].
3. You can parse out four positions ( top_left, top_right, bottom_letf, bottom_right ) in each bounding box.