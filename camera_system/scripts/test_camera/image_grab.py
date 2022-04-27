import pypylon.pylon as py
import numpy as np
import matplotlib.pyplot as plt
import traceback
import time
import cv2

## initialize camera transport layer
tlf = py.TlFactory.GetInstance()
devices = tlf.EnumerateDevices()

cam_count = len(devices)

for device in devices:
    print("camera name = ", device.GetUserDefinedName())
    
    if (device.GetUserDefinedName() == 'Narrow'):
        narrow_cam = py.InstantCamera(tlf.CreateDevice(device))
    elif (device.GetUserDefinedName() == 'Wide'):
        wide_cam = py.InstantCamera(tlf.CreateDevice(device))
    


