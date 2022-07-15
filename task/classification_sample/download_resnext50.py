import torch, time, os, sys
import torchvision.models as models
try:
    from torch2trt import torch2trt
except:
    print("There is no torch2trt, please install via ./docker/trt/patch_pose.sh")
    exit(1)

print("# Convert Torch Model")

# define model 
model_name = 'resnet50.engine'

# convert to TensorRT feeding sample data as input
dirname, filename = os.path.split(os.path.abspath(__file__))    # get target folder
engine_path = os.path.join(dirname, model_name)                 # combine the path

if not os.path.exists(engine_path):

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

else:

    print("TensorRT Engine is exist !")

print()
