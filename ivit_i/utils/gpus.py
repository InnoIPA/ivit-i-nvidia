import GPUtil, logging, os

def get_gpu_info():
    gpus = GPUtil.getGPUs()
    ret = dict()
    for gpu in gpus:
        ret.update({ gpu.name: {
                
                "id": gpu.id,
                "name": gpu.name, 
                "uuid": gpu.uuid, 
                "load": round(gpu.load*100, 3), 
                "memoryUtil": round(gpu.memoryUtil*100, 3), 
                "temperature": gpu.temperature
        }})
    return ret