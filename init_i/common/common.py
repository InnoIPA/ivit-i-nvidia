#
# Copyright 1993-2020 NVIDIA Corporation.  All rights reserved.
#
# NOTICE TO LICENSEE:
#
# This source code and/or documentation ("Licensed Deliverables") are
# subject to NVIDIA intellectual property rights under U.S. and
# international Copyright laws.
#
# These Licensed Deliverables contained herein is PROPRIETARY and
# CONFIDENTIAL to NVIDIA and is being provided under the terms and
# conditions of a form of NVIDIA software license agreement by and
# between NVIDIA and Licensee ("License Agreement") or electronically
# accepted by Licensee.  Notwithstanding any terms or conditions to
# the contrary in the License Agreement, reproduction or disclosure
# of the Licensed Deliverables to any third party without the express
# written consent of NVIDIA is prohibited.
#
# NOTWITHSTANDING ANY TERMS OR CONDITIONS TO THE CONTRARY IN THE
# LICENSE AGREEMENT, NVIDIA MAKES NO REPRESENTATION ABOUT THE
# SUITABILITY OF THESE LICENSED DELIVERABLES FOR ANY PURPOSE.  IT IS
# PROVIDED "AS IS" WITHOUT EXPRESS OR IMPLIED WARRANTY OF ANY KIND.
# NVIDIA DISCLAIMS ALL WARRANTIES WITH REGARD TO THESE LICENSED
# DELIVERABLES, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY,
# NONINFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
# NOTWITHSTANDING ANY TERMS OR CONDITIONS TO THE CONTRARY IN THE
# LICENSE AGREEMENT, IN NO EVENT SHALL NVIDIA BE LIABLE FOR ANY
# SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, OR ANY
# DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THESE LICENSED DELIVERABLES.
#
# U.S. Government End Users.  These Licensed Deliverables are a
# "commercial item" as that term is defined at 48 C.F.R. 2.101 (OCT
# 1995), consisting of "commercial computer software" and "commercial
# computer software documentation" as such terms are used in 48
# C.F.R. 12.212 (SEPT 1995) and is provided to the U.S. Government
# only as a commercial end item.  Consistent with 48 C.F.R.12.212 and
# 48 C.F.R. 227.7202-1 through 227.7202-4 (JUNE 1995), all
# U.S. Government End Users acquire the Licensed Deliverables with
# only those rights set forth herein.
#
# Any use of the Licensed Deliverables in individual and commercial
# software must include, in the user documentation and internal
# comments to the code, the above Disclaimer and U.S. Government End
# Users Notice.
#

from itertools import chain
import argparse
import os, sys

import pycuda.driver as cuda
# import pycuda.autoinit
import numpy as np

import tensorrt as trt
import logging

sys.path.append(os.getcwd())
from ivit_i.utils.timer import Timer
from ivit_i.utils.drawing_tools import get_palette
try:
    # Sometimes python2 does not understand FileNotFoundError
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

EXPLICIT_BATCH = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)

# ------------------------------------------------------------------------------------------------------
# Simple Template for each model
class Model(object):

    def __init__(self, idx=0):
        
        logging.info('Initialize TensorRT ... ')
        t_init = Timer()
        
        # trt
        self.trt_logger = trt.Logger(trt.Logger.WARNING)    # TensorRT logger singleton
        trt.init_libnvinfer_plugins(self.trt_logger, '')    # We first load all custom plugins shipped with TensorRT
        self.runtime = trt.Runtime(self.trt_logger)         # Initialize runtime needed for loading TensorRT engine from file
        
        # init tensorrt 
        cuda.init()
        self.cfx = cuda.Device(idx).make_context()

        # basic
        self.input_size = None
        self.out_size = None
        self.preprocess = None
        self.thres = None
        self.dynamic_shape = None

        logging.info('Initialize TensorRT ... Done ({}s)'.format(t_init.get_cost_time()))

    """ Load model and setup global parameters """
    def load_model(self, config):
        pass

    """ Initialize tensorrt engine """
    def init_engine(self, engine_path, max_batch_size) -> tuple:

        t_build = Timer()
        logging.info("Load TRT engine ...")
        
        # deserialize from serial model
        engine = deseri_engine(self.runtime, engine_path)
        logging.info("  - Loading cache TRT engine from {} ({}s)".format(engine_path, t_build.get_dur_time()))
        
        # allocate buffer
        try:
            context = engine.create_execution_context() 
            inputs, outputs, bindings, stream = allocate_buffers(engine, max_batch_size)    
        except Exception as e:
            raise RuntimeError('fail to allocate CUDA resources') from e
        
        logging.info("  - Allocate buffer ({}s)".format(t_build.get_dur_time()))      
        logging.info("  - Gen execution context ({}s)".format(t_build.get_dur_time()))            
        logging.info("Load TRT engine ... Done. ({}s)".format(t_build.get_cost_time()))
        # return objects for tensorrt inference and palette for drawer
        return tuple([context, inputs, outputs, bindings, stream])

    def store_runtime(self):
        if self.cfx:
            self.cfx.push()

    def clear_runtime(self):
        if self.cfx:
            self.cfx.pop()

    def get_palette(self, config):
        return get_palette(config)

    def inference(self, trt_objects, frame, conf):
        logging.debug("Do Inference")

    def parse_param(self, conf):
        logging.debug("Parse parameters from config")
    
    def release(self):
        self.clear_runtime()
        del self.cfx

# ------------------------------------------------------------------------------------------------------
# Simple helper data class that's a little nicer to use than a 2-tuple.
class HostDeviceMem(object):
    def __init__(self, host_mem, device_mem):
        self.host = host_mem
        self.device = device_mem

    def __str__(self):
        return "Host:\n" + str(self.host) + "\nDevice:\n" + str(self.device)

    def __repr__(self):
        return self.__str__()

# ------------------------------------------------------------------------------------------------------
# deserialize tensorrt engine
def deseri_engine(runtime, path):
    with open(path, 'rb') as serial_engine:             
        engine = runtime.deserialize_cuda_engine(serial_engine.read())
    return engine

# ------------------------------------------------------------------------------------------------------
# Allocates all buffers required for an engine, i.e. host/device inputs/outputs.
def allocate_buffers(engine, batch_size=None):
    
    inputs, outputs, bindings = [], [], []
    stream = cuda.Stream()
    for binding in engine:
        
        size = trt.volume(engine.get_binding_shape(binding)) * ( engine.max_batch_size if not batch_size else batch_size)
        # If size<0 , TensorRT could not allocate buffer
        if size < 0: size *= -1
        dtype = trt.nptype(engine.get_binding_dtype(binding))
        # Allocate host and device buffers
        host_mem = cuda.pagelocked_empty(size, dtype)
        device_mem = cuda.mem_alloc(host_mem.nbytes)
        # Append the device buffer to device bindings.
        bindings.append(int(device_mem))
        # Append to the appropriate list.
        if engine.binding_is_input(binding):
            inputs.append(HostDeviceMem(host_mem, device_mem))
        else:
            outputs.append(HostDeviceMem(host_mem, device_mem))

    return inputs, outputs, bindings, stream

# ------------------------------------------------------------------------------------------------------
# This function is generalized for multiple inputs/outputs.
# inputs and outputs are expected to be lists of HostDeviceMem objects.
def do_inference(context, bindings, inputs, outputs, stream, batch_size=1, dynamic_shape=None):
    # Transfer input data to the GPU.
    [cuda.memcpy_htod_async(inp.device, inp.host, stream) for inp in inputs]
    # dynamic input shape need to setup input shape
    if dynamic_shape!=None:
        context.set_binding_shape(0, dynamic_shape)
        batch_size = dynamic_shape[0]
    # Run inference.
    context.execute_async(batch_size=batch_size, bindings=bindings, stream_handle=stream.handle)
    # Transfer predictions back from the GPU.
    [cuda.memcpy_dtoh_async(out.host, out.device, stream) for out in outputs]
    # Synchronize the stream
    stream.synchronize()
    # Return only the host outputs.
    return [out.host for out in outputs]

# ------------------------------------------------------------------------------------------------------
# This function is generalized for multiple inputs/outputs for full dimension networks.
# inputs and outputs are expected to be lists of HostDeviceMem objects.
def do_inference_v2(context, bindings, inputs, outputs, stream):
    # Transfer input data to the GPU.
    [cuda.memcpy_htod_async(inp.device, inp.host, stream) for inp in inputs]
    # Run inference.
    context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)
    # Transfer predictions back from the GPU.
    [cuda.memcpy_dtoh_async(out.host, out.device, stream) for out in outputs]
    # Synchronize the stream
    stream.synchronize()
    # Return only the host outputs.
    return [out.host for out in outputs]

# ------------------------------------------------------------------------------------------------------
# `retry_call` and `retry` are used to wrap the function we want to try multiple times
def retry_call(func, args=[], kwargs={}, n_retries=3):
    """Wrap a function to retry it several times.

    Args:
        func: function to call
        args (List): args parsed to func
        kwargs (Dict): kwargs parsed to func
        n_retries (int): maximum times of tries
    """
    for i_try in range(n_retries):
        try:
            func(*args, **kwargs)
            break
        except:
            if i_try == n_retries - 1:
                raise
            print("retry...")

# ------------------------------------------------------------------------------------------------------
# Usage: @retry(n_retries)
def retry(n_retries=3):
    """Wrap a function to retry it several times. Decorator version of `retry_call`.

    Args:
        n_retries (int): maximum times of tries

    Usage:
        @retry(n_retries)
        def func(...):
            pass
    """
    def wrapper(func):
        def _wrapper(*args, **kwargs):
            retry_call(func, args, kwargs, n_retries)
        return _wrapper
    return wrapper

# ------------------------------------------------------------------------------------------------------
def GiB(val):
    return val * 1 << 30
