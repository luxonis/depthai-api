#!/usr/bin/env python3

import cv2
import depthai as dai
import numpy as np


'''
If one or more of the additional depth modes (lrcheck, extended, subpixel)
are enabled, then:
 - depth output is FP16. TODO enable U16.
 - median filtering is disabled on device. TODO enable.
 - with subpixel, either depth or disparity has valid data.
Otherwise, depth output is U16 (mm) and median is functional.
But like on Gen1, either depth or disparity has valid data. TODO enable both.
'''

# Closer-in minimum depth, disparity range is doubled (from 95 to 190):
extended_disparity = False
# Better accuracy for longer distance, fractional disparity 32-levels:
subpixel = False
# Better handling for occlusions:
lr_check = False

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - two mono (grayscale) cameras
left = pipeline.createMonoCamera()
left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
left.setBoardSocket(dai.CameraBoardSocket.LEFT)

right = pipeline.createMonoCamera()
right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
right.setBoardSocket(dai.CameraBoardSocket.RIGHT)

# Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
depth = pipeline.createStereoDepth()
depth.setConfidenceThreshold(200)
depth.setOutputDepth(False)
# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
median = dai.StereoDepthProperties.MedianFilter.KERNEL_7x7 # For depth filtering
depth.setMedianFilter(median)

depth.setLeftRightCheck(lr_check)

# Normal disparity values range from 0..95, will be used for normalization
max_disparity = 95

if extended_disparity: max_disparity *= 2 # Double the range
depth.setExtendedDisparity(extended_disparity)

if subpixel: max_disparity *= 32 # 5 fractional bits, x32
depth.setSubpixel(subpixel)

# When we get disparity to the host, we will multiply all values with the multiplier
# for better visualization
multiplier = 255 / max_disparity

left.out.link(depth.left)
right.out.link(depth.right)

# Create output
xout = pipeline.createXLinkOut()
xout.setStreamName("disparity")
depth.disparity.link(xout.input)

# Pipeline is defined, now we can connect to the device
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    # Output queue will be used to get the disparity frames from the outputs defined above
    q = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)
    while True:
        inDepth = q.get()  # blocking call, will wait until a new data has arrived
        frame = inDepth.getFrame()
        frame = (frame*multiplier).astype(np.uint8)
        # Available color maps: https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html
        frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)

        # frame is ready to be shown
        cv2.imshow("disparity", frame)

        if cv2.waitKey(1) == ord('q'):
            break
