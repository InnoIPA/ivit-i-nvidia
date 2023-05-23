# Classification Sample
iVIT Classification Sample, this sample demonstrates how to do inference of image classification models using iVIT [Source](../ivit_source_sample/README.md) and [Displayer](../ivit_displayer_sample/README.md).

## Getting Start
* Clone Repository    
    ```bash
    git clone  https://github.com/InnoIPA/ivit-i-nvidia.git && cd ivit-i-nvidia
    ```
* Run iVIT-I Docker Container
    ```bash
    ./docker/run.sh
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
    cd /workspace/samples/classification_sample
    
    
    chmod u+x ./*.sh

    #Download data and model and covert model.
    ./model_prepare.sh        

    ```
    * More infomation about model_prepare.sh
    ```bash
    ./model_prepare.sh --help
        """
        -m		download model.
        -d		download data.
        -c		convert  model.
        """
    ```
* Setting Varaible
    ```bash
    
    EXEC_PY="python3 ./classification_demo.py"

    ROOT=/workspace
    MODEL=${ROOT}/model/resnet/resnet34.trt
    LABEL=${ROOT}/model/resnet/imagenet.txt
    INPUT=${ROOT}/data/cat.jpg
    ```

* Run Sample
    ```bash
    ${EXEC_PY} -m ${MODEL} -l ${LABEL} -i ${INPUT}
    ```

## Usage
* Help
    ```bash
    ${EXEC_PY} -h
    ```

* Top 5 Labels
    ```bash
    ${EXEC_PY} -m ${MODEL} -l ${LABEL} -i ${INPUT} \
    -topk 5
    ```

## Format of output 
*  The format of result after model predict like below.

    | Name |Type | Description |
    |--- |--- | --- |
    | Input|list|[ turple ( id:int , label:str, score:float ) , ... ]|

* Item Description  
    |Name|Example|Description|
    |---|---| --- |
    |id|0|The sort index of the labels|
    |label|cat|The name of the predict label|
    |score|0.59221|The confidence of the prediction|
