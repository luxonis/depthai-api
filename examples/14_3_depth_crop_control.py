#!/usr/bin/env python3

"""
This example shows usage of depth camera in crop mode with the possibility to move the crop.
Use 'WASD' in order to do it.
"""

import cv2
import depthai as dai
import numpy as np

stepSize = 0.02

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - two mono (grayscale) cameras
left = pipeline.createMonoCamera()
left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
left.setBoardSocket(dai.CameraBoardSocket.LEFT)

right = pipeline.createMonoCamera()
right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
right.setBoardSocket(dai.CameraBoardSocket.RIGHT)

# Crop range
topLeft = dai.Point2f(0.4, 0.4)
bottomRight = dai.Point2f(0.6, 0.6)

manip = pipeline.createImageManip()
manip.initialConfig.setCropRect(topLeft.x, topLeft.y, bottomRight.x, bottomRight.y)
manip.setMaxOutputFrameSize(right.getResolutionHeight()*right.getResolutionWidth()*3)


# Create a node that will produce the depth map
stereo = pipeline.createStereoDepth()
stereo.setConfidenceThreshold(200)
stereo.setOutputDepth(True)

left.out.link(stereo.left)
right.out.link(stereo.right)


# Control movement
controlIn = pipeline.createXLinkIn()
controlIn.setStreamName('control')
controlIn.out.link(manip.inputConfig)

# Create outputs
xout = pipeline.createXLinkOut()
xout.setStreamName("depth")
stereo.depth.link(manip.inputImage)
manip.out.link(xout.input)

# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    # Output queue will be used to get the depth frames from the outputs defined above
    q = device.getOutputQueue(xout.getStreamName(), maxSize=4, blocking=False)

    sendCamConfig = False

    while True:
        inDepth = q.get()  # blocking call, will wait until a new data has arrived
        # data is originally represented as a flat 1D array, it needs to be converted into HxW form
        depthFrame = inDepth.getFrame()
        # frame is transformed, the color map will be applied to highlight the depth info
        depthFrameColor = cv2.normalize(depthFrame, None, 255, 0, cv2.NORM_INF, cv2.CV_8UC1)
        depthFrameColor = cv2.equalizeHist(depthFrameColor)
        depthFrameColor = cv2.applyColorMap(depthFrameColor, cv2.COLORMAP_HOT)
        controlQueue = device.getInputQueue(controlIn.getStreamName())

        # frame is ready to be shown
        cv2.imshow("depth", depthFrameColor)

        # Update screen
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('w'):
            if topLeft.y - stepSize >= 0:
                topLeft.y -= stepSize
                bottomRight.y -= stepSize
                sendCamConfig = True
        elif key == ord('a'):
            if topLeft.x - stepSize >= 0:
                topLeft.x -= stepSize
                bottomRight.x -= stepSize
                sendCamConfig = True
        elif key == ord('s'):
            if bottomRight.y + stepSize <= 1:
                topLeft.y += stepSize
                bottomRight.y += stepSize
                sendCamConfig = True
        elif key == ord('d'):
            if bottomRight.x + stepSize <= 1:
                topLeft.x += stepSize
                bottomRight.x += stepSize
                sendCamConfig = True


        if sendCamConfig:
            cfg = dai.ImageManipConfig()
            cfg.setCropRect(topLeft.x, topLeft.y, bottomRight.x, bottomRight.y)
            controlQueue.send(cfg)
            sendCamConfig = False