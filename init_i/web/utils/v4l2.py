import subprocess

def get_v4l2() -> list:
    ret = subprocess.run("ls /dev/video*",  text=True, shell=True, stdout=subprocess.PIPE).stdout
    ret_list = ret.strip().split('\n')
    return ret_list
