import json, os, logging

VID_EXT=['.mp4', '.avi']
IMG_EXT=['.jpg', '.png', '.jpeg']

def load_json(path:str) -> dict:
    
    # debug
    if not os.path.exists(path):
        raise Exception('File is not exists !')
    elif os.path.splitext(path)[1] != '.json':
        raise Exception("It's not a json file ({})".format(path))
    
    with open(path) as f:
        data = json.load(f)  # load is convert dict from json "file"
    
    return data

def write_json(cnt:dict, path:str) -> None:
    
    with open(path, 'w') as f:
        json.dump(cnt, f)    # dump is write dict into file

def cmp_json(cnt:dict, path:str) -> bool:
    return (load_json(path)==cnt)

def load_txt(path:str) -> list:
    
    if not os.path.exists(path):
        msg = "Can not find label file."
        raise Exception(msg)
        logging.error(msg, stack_info=True)
    
    ret = []
    with open(path) as f:
        lines = f.readlines()
        [ ret.append(line.rstrip() ) for line in lines ]
        
    if ret == []:
        msg = "Failed to load txt file."
        raise Exception(msg)
        logging.error(msg, stack_info=True)

    return ret

def parse_input_data(source:str):
    
    def print_error(msg):
        logging.error(msg)
        raise Exception(msg)

    def check_file(path):
        if not os.path.exists(path):
            print_error("The file is not exist. ({})".format(path))

    if not source:
        print_error("Can not parse source in app configuration, please check again.")

    # video, camera, image
    name, ext = os.path.splitext(source)
    
    if not bool(ext):       
        return "v4l2" if name!='test' else "test"
    
    elif ext in VID_EXT:
        check_file(source)
        return "video"
    
    elif ext in IMG_EXT:
        check_file(source)
        return "image"
    else:
        print_error("Unexcepted input data, the supported format is: {}, {}".format(VID_EXT, IMG_EXT))

def parse_config(cfg:dict) -> dict:
    
    fw = cfg['framework']
    if not (fw in cfg.keys()):
        return cfg

    cfg.update(cfg[fw])
    cfg.pop(fw, None)
    return cfg

if __name__ == '__main__':
    
    path = "./models/mask_classifier_by_max/mask_classifier.txt"
    
    print(load_txt(path))