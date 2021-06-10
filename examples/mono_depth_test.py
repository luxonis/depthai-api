#!/usr/bin/env python3

import cv2
import depthai as dai
import time
from pathlib import Path
import numpy as np

# Closer-in minimum depth, disparity range is doubled (from 95 to 190):
extended_disparity = False
# Better accuracy for longer distance, fractional disparity 32-levels:
subpixel = False
# Better handling for occlusions:
lr_check = False

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
monoLeft = pipeline.createMonoCamera()
monoRight = pipeline.createMonoCamera()
depth = pipeline.createStereoDepth()

xout = pipeline.createXLinkOut()
xoutLeft = pipeline.createXLinkOut()
xoutRight = pipeline.createXLinkOut()

xoutLeft.setStreamName('left')
xoutRight.setStreamName('right')
xout.setStreamName("disparity")

# Properties
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

depth.setConfidenceThreshold(200)
# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
depth.setMedianFilter(dai.StereoDepthProperties.MedianFilter.KERNEL_7x7)
depth.setLeftRightCheck(lr_check)
depth.setExtendedDisparity(extended_disparity)
depth.setSubpixel(subpixel)


# Linking
monoRight.out.link(xoutRight.input)
monoLeft.out.link(xoutLeft.input)
monoLeft.out.link(depth.left)
monoRight.out.link(depth.right)
depth.disparity.link(xout.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queues will be used to get the grayscale frames from the outputs defined above
    qLeft = device.getOutputQueue(name="left", maxSize=4, blocking=False)
    qRight = device.getOutputQueue(name="right", maxSize=4, blocking=False)
    q = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)

    dirName = "mono_data"

    while True:
        # Instead of get (blocking), we use tryGet (nonblocking) which will return the available data or None otherwise
        inLeft = qLeft.tryGet()
        inRight = qRight.tryGet()
        inDepth = q.get() 
        frame = inDepth.getFrame()
        # Normalization for better visualization
        frame = (frame * (255 / depth.getMaxDisparity())).astype(np.uint8)

        if inLeft is not None:
            cv2.imshow("left", inLeft.getCvFrame())

        if inRight is not None:
            cv2.imshow("right", inRight.getCvFrame())
        
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('p'):
            cv2.imwrite(f"{dirName}/right/{int(time.time() * 1000)}.png", inRight.getFrame())
            cv2.imwrite(f"{dirName}/left/{int(time.time() * 1000)}.png", inLeft.getFrame())
            cv2.imwrite(f"{dirName}/disp/{int(time.time() * 1000)}.png", frame)
