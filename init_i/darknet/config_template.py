TEMPLATE = {
    "tag": "darknet",
    "tensorrt": {
        "model_path": "./task/yolov3-tiny/yolov3-tiny-416.trt",
        "label_path": "./task/yolov3-tiny/coco.txt",
        "device": "NVIDIA GeForce GTX 1050 Ti",
        "input_size": "3,416,416",
        "preprocess": "caffe",
        "thres": 0.6,
        "nms_thres": 0.8
    }
}