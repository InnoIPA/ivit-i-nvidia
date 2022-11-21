import torch, time, os, sys, gdown, threading
import torchvision.models as models
try:
    from torch2trt import torch2trt
except:
    print("There is no torch2trt, please install via ./docker/trt/patch_pose.sh")
    exit(1)

def download_label(url, path):
    if( not os.path.exists(path)):
        print('Downloading Label File')
        gdown.download( url, path)
    else:
        print('Label file is already exist!!!')

# define model 
model_dir   = './model/resnet50'
model_name  = 'resnet50.engine'
label_name  = 'imagenet.txt'
label_url   = 'https://drive.google.com/uc?id=1n83YDxZsWvZ5UtPqN0Vc0iFVbg3WOo2a'

# convert to TensorRT feeding sample data as input
# model_dir, filename = os.path.split(os.path.abspath(__file__))    # get target folder
engine_path = os.path.join(model_dir, model_name)                 # combine the path
label_path = os.path.join(model_dir, label_name)

if os.path.exists(engine_path) and os.path.exists(label_path):
    print("TensorRT Engine is exist !\n")
    exit(0)

# create folder
if( not os.path.exists(model_dir)): 
    os.makedirs(model_dir)
    
# download label with thread
label_thread = threading.Thread( target=download_label, args= (label_url, label_path, ), daemon=True )
label_thread.start()

# create some regular pytorch model...
t0 = time.time()
model = models.resnext50_32x4d(pretrained=True).eval().cuda()
print("Download ResNeXt50 ... {}s".format( round(time.time()-t0, 3) ))

# create example data
x = torch.ones((1, 3, 224, 224)).cuda()

# convert
t0 = time.time()
model_trt = torch2trt(model, [x])
print('Convert to TensorRT ... {}s'.format( round(time.time()-t0, 3) ))

# save the tensorrt engine
t0 = time.time()
with open(engine_path, "wb") as f:                              # save tensorrt engine
    f.write(model_trt.engine.serialize())
print('Save the tensorrt engine ... {}s'.format( round(time.time()-t0, 3) ))

label_thread.join()
print('Done. \n')