import wget, argparse, os, logging, gdown

DOWNLOAD_MAP = {
    "yolov3": {
        "weight": "https://pjreddie.com/media/files/yolov3.weights",
        "config": "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg",
    },
    "yolov3-tiny": {
        "weight": "https://pjreddie.com/media/files/yolov3-tiny.weights",
        "config": "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov3-tiny.cfg",
    },
    "yolov4": {
        "weight": "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights",
        "config": "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg",
    },
    "yolov4-tiny": {
        "weight": "https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights",
        "config": "https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg",
    },
    "label":{
        "name": "coco.txt",
        "org_url": "https://drive.google.com/file/d/1OY9Qg6O-x1jDLchZqe3I8gKvvKzr44_C/view?usp=sharing",
        "url": 'https://drive.google.com/uc?id=1OY9Qg6O-x1jDLchZqe3I8gKvvKzr44_C'
    }
}

def key_in_name(name:str, keys):
    keys = [ keys ] if isinstance(keys, str) else keys
    for key in keys:
        if key in name:
            return True
    return False

def check_path(path, need_raise=False, log=True):
    flag = True if os.path.exists(path) else False
    msg = 'check "{}" ... {}'.format(path, 'true' if flag else 'failed')
    
    if log: 
        print(msg)
    if need_raise and not flag: 
        raise Exception(msg)
    return flag

# -------------------------------------------------------
# Modify config and soft link a new weight
def modify_size(model, size, log=True):

    # basic
    model_name = model
    data = []
    weight_ext, config_ext = 'weights', 'cfg'
    height, width = size.split('x') if 'x' in size else (size, size)
    line_batch, line_width, line_height = (-1), 8, 9    # the basic line for yolov3
    
    # if the target model is yolov4
    if "v4" in model_name:
        # 2,7,8 is for normal one
        (line_batch, line_width, line_height) = (6, 8, 9) if key_in_name(name=model_name, keys=['tiny', 'csp', 'p5', 'mish']) else (2, 7, 8)
    
    # create a new name and combine the path
    new_name = "{}-{}".format(  model_name, height if height==width else size )
    org_weight = os.path.abspath(f"{model_name}.{weight_ext}")
    org_config = os.path.abspath(f"{model_name}.{config_ext}")
    trg_weight = os.path.abspath(f"{new_name}.{weight_ext}")
    trg_config = os.path.abspath(f"{new_name}.{config_ext}")
    
    check_path(org_weight, need_raise=True)
    check_path(org_config, need_raise=True)
    
    if( not check_path(trg_config)):
        with open(org_config, 'r') as file:
            data = file.readlines()
            # modify width and height
            data[ line_width-1 ]="width={}\n".format(width)
            data[ line_height-1 ]="height={}\n".format(height)
            data[-1]="\n"
            print(' * width -> {}'.format( width ))
            print(' * height -> {}'.format( height ))
            # yolo v4 need to change the batch
            if line_batch != (-1):
                data[ line_batch-1 ]="batch=1\n"
                print(' * batch -> {}'.format( 1 ))
        # double check
        if data==[]: raise Exception('read {} content failed'.format( org_config ))

        # write a new config
        with open(trg_config, 'w') as file:
            file.writelines(data)
    else:
        print("Config already exist")

    # new weight file if needed
    if not check_path( trg_weight, log=False ):        
        # link weight
        # print("\nLink a new weight file: {}".format(trg_weight))
        # os.symlink( org_weight, trg_weight )
        print("\nRename the weight file: {}".format(trg_weight))
        os.rename(org_weight, trg_weight)
        
        # clear os config
        os.remove(org_config)
    
    return new_name

# -------------------------------------------------------
# Download weight if needed
def download_model_by_name(name, folder):
    
    # Create folder if needed
    if not check_path(folder): 
        print('\nCreate a new folder ({})'.format(folder))
        os.makedirs(folder)

    # Download Weight and Config
    for key in ['weight', 'config']:
        url = DOWNLOAD_MAP[name][key]
        file_name = os.path.join(folder, url.split('/')[-1] ) 

        if not check_path( file_name , log=False):
            print('Start to download {} ...'.format(file_name), end='')
            wget.download(url, folder, False) 
            print('Done')

def download_label(url, path):
    if( not os.path.exists(path)):
        gdown.download( url, path)

if __name__ == "__main__":
    # ---------------------------------------------------
    # Parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help="model name", default="yolov3",type=str)
    parser.add_argument("-s", "--size", help="input size", default="416x416", type=str)
    parser.add_argument("-f", "--folder", help="folder to place the weight and the config", default=".", type=str)
    args = parser.parse_args()
    
    # ---------------------------------------------------
    # Download weight if needed
    print('\nStart to download the model weights and configuration.')
    download_model_by_name(args.model, args.folder)

    # ---------------------------------------------------
    # Modify config and soft link a new weight
    # return the target model name ( without extension )
    print('\nStart to modify configuration and create a soft link for weight file.')
    trg_model = modify_size(os.path.join(args.folder, args.model), args.size)

    print('\nDownload label file')
    download_label(
        DOWNLOAD_MAP["label"]["url"] , 
        os.path.join(args.folder, DOWNLOAD_MAP["label"]["name"]))

    print('\nAll Done.\n')