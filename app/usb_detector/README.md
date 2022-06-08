# TAO-YOLOv4 for iVINNO-TensorRT
YOLOv4 model which trained from NVIDIA TAO or iTAO.
# Enter the container
```bash
sudo ./docker/trt/run.sh -f nvidia -v v0.1 -m
```

# Download Model and Label
```
./app/trt/usb_detecotr/download_model.sh
```
# Download meta data
```
./app/trt/usb_detecotr/download_testing_data.sh
```
# Convert Model
```
./converter/tao-converter \
-k nvidia_tlt \
-p Input,1x3x608x608,8x3x608x608,16x3x608x608 \
-d 3,608,608 \
-o BatchedNMS \
-e ./app/trt/usb_detector/usb.engine \
-t fp32 \
-i nchw \
-m 1 \
./app/trt/usb_detector/yolov4_darknet53_e100_pruned_fp16.etlt
```
# Modified Configuration
```
input_data: ./app/trt/usb_detector/output.mp4
```
# --------------------- -------------------------

## Pre-requirements

### 1. Prepare Model and Label
```shell
.
|-- README.md
|-- mask_classifier.txt # label file
`-- model.etlt          # etlt model

0 directories, 3 files
```

### 2. Convert Model
* Note that YOLOv4 has a dynamic input shape, you should add `-p` when converting the model.
    ```shell
    # For Example
    $ cd /ivinno-trt

    $ ./converter/tao-converter \
    -k nvidia_tlt \
    -p Input,1x3x608x608,8x3x608x608,16x3x608x608 \
    -d 3,608,608 \
    -o BatchedNMS \
    -e ./app/trt/usb_detector/usb.engine \
    -t fp32 \
    -i nchw \
    -m 1 \
    ./app/trt/usb_detector/yolov4_darknet53_e100_pruned_fp16.etlt

    # ...
    # [INFO] Detected input dimensions from the model: (-1, 3, 608, 608)
    # [INFO] Model has dynamic shape. Setting up optimization profiles.
    # [INFO] Using optimization profile min shape: (1, 3, 608, 608) for input: Input
    # [INFO] Using optimization profile opt shape: (8, 3, 608, 608) for input: Input
    # [INFO] Using optimization profile max shape: (16, 3, 608, 608) for input: Input
    # [INFO] Detected 1 inputs and 4 output network tensors.
    ```

## Run Classfication with iVINNO configuration
1. Update informations about model and label in `/ivinno-trt/config/model_config/yolov4.json`
    ```text
    # For Example
    model_path -> "./models/TAO-YOLOv4/yolov4_darknet53_e100_pruned_fp16.trt"
    label_path -> "./models/TAO-YOLOv4/model_output_labels.txt"
    input_size -> "3,608,608"
    ```
2. Run demo.py
```
$ cd /ivinno-trt
$ python3 demo.py -c ./config/app_config/trt_yolov4.json
```

# For Developer

## Reference
1. The model in TAO-Classficiation should be trained from NVIDIA TAO or iTAO and must be the .

## Pre-processing
> Classic Caffe mode
1. Convert the images from RGB to BGR.
2. Rescale to the target size via `cv2.resize`.
3. zero-center each color channel with respect to the ImageNet dataset.
    * BGR -> [103.939, 116.779, 123.68]

## Post-processing
1. Output is an array means confidence in each category.
