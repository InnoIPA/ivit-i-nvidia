import sys, os
import logging, shutil, cv2
import numpy as np
import tensorrt as trt

# ==========================================================================================
# Main
""" The Entry of Pre-processing """
def preproc(image, size=(224,224), mode='caffe', is_rgb=None, is_chw=None, is_mean=None):
    
    mode = mode.lower()     # mapping data

    if 'caffe' in mode:
        trg = caffe
    elif 'torch' in mode:
        trg = torch_proc
    else:
        logging.error('Unknown pre-process mode, excepted [`caffe`, `tf`, `torch`], but got `{}`'.format(mode))
        raise
    
    # return ret_image.astype(get_nptype(dtype))
    return trg(image, size, is_rgb, is_chw, is_mean)

""" Caffe2 Caffe """
def caffe(img, size, is_rgb=None, is_chw=None, is_mean=None):
    """ --------------------------------------------------------------------------------------
    1. Caffe Uses BGR Order: 使用 OpenCV 導入則可以不用開啟。
    2. Caffe Prefers CHW Order: 通道、高度、寬度。
    3. Sizing: 通常尺寸為(224,224)，但主要是隨著當初模型如何訓練而修改。
    4. Rescling: 我以最小邊去縮放。 Caffe還有分以高度去縮放(Landscape)，或者以寬度去縮放(Portrait)。
    5. Cropping: 裁切中心的位置。
    6. Offset: 通常使用 ImageNet 的數據集的BGR均值 進行 減均值的動作。
    -------------------------------------------------------------------------------------- """
    # logging.debug('Using Caffe2 pre-processing ...')
    is_rgb = is_rgb if is_rgb != None else False
    is_chw = is_chw if is_chw != None else True
    is_mean = is_mean if is_mean != None else True
    # --------------------------------------------------
    _img = img.astype(get_nptype('fp32'))
    _img = cv2.resize(_img, size[::-1])
    # _img = custom_resize(_img, size)
    # _img = crop_center(_img, size)
    # --------------------------------------------------
    if is_mean:
        trg_offset  = ( 103.939, 116.779, 123.68 )  # bgr
        for i in range(3):
            _img[:,:,i]=_img[:,:,i]-trg_offset[i]    
    # --------------------------------------------------
    _img = _img.transpose( (2, 0, 1) ) if is_chw else _img   
    # --------------------------------------------------
    
    return _img

""" Torch Mode """
def torch_proc(img, size, is_rgb=None, is_chw=None, is_mean=None):
    """ --------------------------------------------------------------------------------------
    1. 縮放到正確尺寸，為了後續不容易跑版 採用直接 resize 的方。
    1. 正規化到 0 ~ 1 之間。
    2. 依據 ImageNet 的數據級分佈進行正規化 (RGB Format)。
    3. CHW Format。
    -------------------------------------------------------------------------------------- """
    # logging.debug('Using Torch pre-processing ...')
    is_rgb = is_rgb if is_rgb != None else True
    is_chw = is_chw if is_chw != None else True
    is_mean = is_mean if is_mean != None else True
    # --------------------------------------------------
    _img = img.astype(get_nptype('fp32'))
    _img = cv2.resize(_img, size[::-1])       
    _img = cv2.cvtColor(_img, cv2.COLOR_BGR2RGB) if is_rgb else _img
    # --------------------------------------------------
    _img = _img/255.0
    if is_mean:
        mean = np.array([0.485, 0.456, 0.406])      # rgb
        std = np.array([0.229, 0.224, 0.225])  
        for i in range(3):
            _img[:,:, i] = (_img[:,:, i]-mean[i])/std[i]  
    # --------------------------------------------------
    _img = np.transpose(_img, (2,0,1)) if is_chw else _img
    # --------------------------------------------------
    return _img

# ==========================================================================================
# Utils
""" Return the numpy type mapping from tensorrt type using `tensorrt.nptype` """
def get_nptype(data_type):
    data_type = data_type.lower()
    trt_type = ""
    if data_type=="fp32":
        # logging.debug('Using float32.')
        trt_type = trt.float32
    elif data_type=="fp16":
        # logging.debug('Using float16.')
        trt_type = trt.float32
    elif data_type=="int8":
        # logging.debug('The format of input data not support `int8`, fix it to `float32`.')
        trt_type = trt.float32
    else:
        logging.error('Unknown data type, excepted [`fp32`, `fp16`, `int8`] but get `{}`.'.format(data_type))
        raise
    return trt.nptype(trt_type)

""" Resize image to target shape base on long side. ( height, width ) """
def custom_resize(img, size=(256,256)):

    logging.debug('Resizing ...')
    
    # parse image shape and check
    src_h, src_w, src_c = img.shape
    trg_h, trg_w = size

    if src_h==trg_h and src_w==trg_w:
        logging.debug('The image is the same as the target size.')
        return img
    
    # calculate scale proportion
    # 如果 src 比 trg 大，需要縮小，則以 縮放比例 小的為主
    if (src_h*src_w)>(trg_h*trg_w):     
        scale_w, scale_h = src_w/trg_w, src_h/trg_h
        scale = scale_h if scale_h < scale_w else scale_w
    # 如果 src 比 trg 小，需要放大，則以 縮放比例 大的為主
    else:
        scale_w, scale_h = trg_w/src_w, trg_h/src_h
        scale = scale_h if scale_h > scale_w else scale_w
    
    trg_size = ( round(src_w*scale), round(src_h*scale) )

    # scale and return
    res = cv2.resize(img, trg_size )
    logging.debug('The image shape: {} -> {}'.format(img.shape, res.shape))
    return res

""" Crop the center of the image """
def crop_center(img, size=(224,244)):
    logging.debug('Crop center ...')

    # parse image shape and check
    img_h, img_w, img_c = img.shape
    trg_h, trg_w = size

    if img_h==trg_h and img_w==trg_w:
        logging.debug('The image is the same as the target size.')
        return img
    # calculate the center position
    ## find center
    cen_h, cen_w = img_h//2, img_w//2
    pad_h, pad_w = trg_h//2, trg_w//2
    
    res = img[cen_h-pad_h:cen_h+pad_h, cen_w-pad_w:cen_w+pad_w]
    
    # return 
    logging.debug('The image shape: {} -> {}'.format(img.shape, res.shape))
    return res