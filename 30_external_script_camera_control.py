#!/usr/bin/env python3
import cv2
import depthai as dai
import numpy as np
import time

import inspect

from external_script_samples import *
from external_script_utils import *

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - color camera
cam = pipeline.create(dai.node.ColorCamera)

# Script node
script = pipeline.create(dai.node.Script)

# no delay between captures
embeddableMethod = inspect.getsource(stillCapture)

# 1 second delay between captures
# embeddableMethod = inspect.getsource(stillCaptureEverySecond)

embeddableMethod = unindentMethod(embeddableMethod)
print(embeddableMethod)

script.setScriptData(embeddableMethod)

# XLinkOut
xout = pipeline.create(dai.node.XLinkOut)
xout.setStreamName('still')

# Connections
script.outputs['out'].link(cam.inputControl)
cam.still.link(xout.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()
    while True:
        img = device.getOutputQueue("still").get()
        cv2.imshow('still', img.getCvFrame())
        if cv2.waitKey(1) == ord('q'):
            exit(0)
