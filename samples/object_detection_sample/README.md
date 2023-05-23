# Object Detection Sample
iVIT Object Detection Sample, this sample demonstrates how to do inference of image object detection models using iVIT [Source](../ivit_source_sample/README.md) and [Displayer](../ivit_displayer_sample/README.md).

## Getting Start
* Clone Repository    
    ```bash
    git clone  https://github.com/InnoIPA/ivit-i-nvidia.git && cd ivit-i-nvidia
    ```
* Run iVIT-I Docker Container
    ```bash
    ./docker/run.sh    # Enter the docker container
    ```
    * More options : 
        ```bash
        -b	#run in background
        -q	#Qucik launch iVIT-I
        -h	#help.
        ```
* Download Data
    ```bash
    # Move to target folder
    cd /workspace/samples/object_detection_sample
    
    chmod u+x ./*.sh

    #Download data and model and covert model.
    ./model_prepare.sh -n yolov3-tiny -s 416

    ```
    * More infomation about model_prepare.sh
    ```bash
    ./model_prepare.sh --help
        """
        -m | --model	:Download model
        -d | --data		:Download data
        -c | --covert	:Convert model
        -n | --name		:Model name
        -s | --size		:Model size
        --support       :Show all model we support.
        """
    ```
    * Show all model we support
    ```bash
    ./model_prepare.sh --support
        """
        Model Name	    | Size |        	
        ---------------------------
        yolov3		| 416  |
        yolov3-tiny		| 416  |
        yolov4		| 416  |
        yolov4-tiny		| 416  |
        """

    ```
# Usage
* Base on YOLOv3-tiny
    
    * Setting Varaible
        ```bash
        EXEC_PY="python3 ./object_detection_demo.py"
        ROOT=/workspace
        INPUT=${ROOT}/data/car.mp4
        MODEL=${ROOT}/model/yolov3-tiny/yolov3-tiny-416.trt
        LABEL=${ROOT}/model/yolov3-tiny/coco.txt
        ARCHITECTURE=yolov3

        ```
    * Run Sample:
        
        ```bash
        
        ${EXEC_PY} -m ${MODEL} -l ${LABEL} -at ${ARCHITECTURE} -i ${INPUT} 
        ```

* Base on YOLOv4-tiny
    
    
    * Download data and model and covert model.
    ```bash
    cd /workspace/samples/object_detection_sample
    ./model_prepare.sh -n yolov4-tiny -s 416
    ```
    * Setting Varaible
    ```bash
    # YOLOv4 Tiny:
    EXEC_PY="python3 ./object_detection_demo.py"
    ROOT=/workspace
    INPUT=${ROOT}/data/car.mp4
    MODEL=${ROOT}/model/yolov4-tiny/yolov4-tiny-416.trt
    LABEL=${ROOT}/model/yolov4-tiny/coco.txt
    ARCHITECTURE=yolov4
    THRES=0.7
    ```
* Add Confidence Threshold
    ```bash
    # Define threshold
    ${EXEC_PY} -m ${MODEL} -l ${LABEL} -at ${ARCHITECTURE} -i ${INPUT} -t ${THRES}
    ```

## Format of output 
*  The format of result after model predict like below.

| Type | Description |
| --- | --- |
|list|Object's properties : xmin ,ymin ,xmax ,ymax ,score ,id ,label |
* Example:
    ```bash
        detection        # (type object)                   
        detection.label  # (type str)           value : person   
        detection.score  # (type numpy.float64) value : 0.960135 
        detection.xmin   # (type int)           value : 1        
        detection.ymin   # (type int)           value : 78       
        detection.xmax   # (type int)           value : 438  
        detection.ymax   # (type int)           value : 50     
    ```