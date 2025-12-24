#!/usr/bin/env python3
"""Check GPU configuration for ComfyUI"""
import os
import sys

sys.path.insert(0, '/media/zudva/git/git/ComfyUI')
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'

import torch

print(f"CUDA_VISIBLE_DEVICES: {os.environ.get('CUDA_VISIBLE_DEVICES', 'not set')}")
print(f"PyTorch CUDA available: {torch.cuda.is_available()}")
print(f"Number of CUDA devices: {torch.cuda.device_count()}")
print()

for i in range(torch.cuda.device_count()):
    print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
    props = torch.cuda.get_device_properties(i)
    print(f"  Total memory: {props.total_memory / 1024**3:.2f} GB")
    print(f"  Compute capability: {props.major}.{props.minor}")
    print()
