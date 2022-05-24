import logging, GPUtil, sys
from init_i.cls.classification import Classification
from init_i.seg.segmentation import Segmentation
from init_i.seg.semsegmentation import SemSegmentation
from init_i.obj.yolov4 import YoloV4
from init_i.pose.bodypose import BodyPose
from init_i.darknet.darknet import Darknet

# get gpu list
def get_gpu_info():
    gpus = GPUtil.getGPUs()
    ret = list()
    for gpu in gpus:
        ret.append({
            "id": gpu.id,
            "name": gpu.name, 
            "uuid": gpu.uuid, 
            "load": round(gpu.load*100, 3), 
            "memoryUtil": round(gpu.memoryUtil*100, 3), 
            "temperature": gpu.temperature
        })
    return ret

def find_gpu(in_gpu_name):
    ret = False
    gpu_idx = None
    for gpu in get_gpu_info():
        if in_gpu_name == gpu["name"]:
            logging.info('Found GPU ... change the name ({}) into index {}'.format(gpu['name'], gpu['id']))
            gpu_idx = int(gpu['id'])
            ret = True
    return ret, gpu_idx

def get(prim_conf):
    
    model_conf = prim_conf[ prim_conf['framework'] ]    
    ret, gpu_idx = find_gpu(model_conf['device'])
    if not ret:
        logging.error('Could not found GPU name ... {}'.format(model_conf['device']))
        logging.info('Set the gpu index to 0 ( {} )'.format(get_gpu_info()[0]['name']))
        gpu_idx = 0
    
    if 'cls' in prim_conf['tag']:
        trg = Classification(gpu_idx)
    elif 'obj' in prim_conf['tag']:
        trg = YoloV4(gpu_idx)
    elif 'seg' in prim_conf['tag']:
        trg = SemSegmentation(gpu_idx) if 'sem' in prim_conf['tag'] else Segmentation(gpu_idx)    
    elif 'pose' in prim_conf['tag']:
        trg = BodyPose(gpu_idx)
    elif 'darknet' in prim_conf['tag']:
        trg = Darknet(gpu_idx)
    else:
        msg = 'Unexcepted `tag` in {}'.format(prim_conf['prim'])
        logging.error(msg)
        raise Exception(msg)
    return trg