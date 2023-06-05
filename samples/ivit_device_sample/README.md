# IVIT-I iDEVICE 
iVIT-I iDEVICE Sample, this sample demonstrates how to do use iDEVICE to monitor device on [iVIT](../../README.md).

# Usage
* Create instance for iDevice.
    ```bash
    #import iDevice from ivit
    from ivit_i.utils import iDevice 

    idev = iDevice()

    ```
* Another useful function.  
    1. Use `idev.get_available_device()` can get all uid of device with list, and the format of return like below.  

    

        ```python
        ['NVIDIA GeForce RTX 2070 SUPER']

        ```
    2. Use `idev.get_device_info()` can get all device information,and the format of return like below.
       If you have multi-device and you just want to check specific device.you can use `idev.get_device_info(uid)`. (uid you can get from
       `get_available_device()`.)

        ```python

        
        #Accelerator information.      
            'NVIDIA GeForce RTX 2070 SUPER':{
                    'id': 0,                                            # the idex wget from device.s
                    'uid': 'NVIDIA GeForce RTX 2070 SUPER',            # the name get from device. 
                    'load': 0,                                          # loading capacity get from device.
                    'memoryUtil': 0,                                    # amount of memory usage get from device.
                    'temperature': 30.857142857142858                   # temperature get from device
                  }
        


        ```
   

    