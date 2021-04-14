#!/usr/bin/env python3

"""
This example shows usage of mono camera in crop mode with the possibility to move the crop.
Uses 'WASD' controls to move the crop window, 'T' to trigger autofocus, 'IOKL,.' for manual exposure/focus:
  Control:      key[dec/inc]  min..max
  exposure time:     I   O      1..33000 [us]
  sensitivity iso:   K   L    100..1600
To go back to auto controls:
  'E' - autoexposure
"""


import cv2
import depthai as dai

# Step size ('W','A','S','D' controls)
stepSize = 0.02
# Manual exposure/focus set step
expStep = 500  # us
isoStep = 50

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - two mono (grayscale) camera
camRight = pipeline.createMonoCamera()
camRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
camRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
camLeft = pipeline.createMonoCamera()
camLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
camLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

# Crop range
topLeft = dai.Point2f(0.4, 0.4)
bottomRight = dai.Point2f(0.6, 0.6)

manipRight = pipeline.createImageManip()
manipRight.initialConfig.setCropRect(topLeft.x, topLeft.y, bottomRight.x, bottomRight.y)
manipLeft = pipeline.createImageManip()
manipLeft.initialConfig.setCropRect(topLeft.x, topLeft.y, bottomRight.x, bottomRight.y)
manipRight.setMaxOutputFrameSize(camRight.getResolutionHeight()*camRight.getResolutionWidth()*3)

# Camera movement config (wasd)
configIn = pipeline.createXLinkIn()
configIn.setStreamName('config')
configIn.out.link(manipRight.inputConfig)
configIn.out.link(manipLeft.inputConfig)

# Camera control (exp, iso, focus)
controlIn = pipeline.createXLinkIn()
controlIn.setStreamName('control')
controlIn.out.link(camRight.inputControl)
controlIn.out.link(camLeft.inputControl)

# Linking with USB
camRight.out.link(manipRight.inputImage)
camLeft.out.link(manipLeft.inputImage)

# Create outputs
manipOutRight = pipeline.createXLinkOut()
manipOutRight.setStreamName("right")
manipRight.out.link(manipOutRight.input)

manipOutLeft = pipeline.createXLinkOut()
manipOutLeft.setStreamName("left")
manipLeft.out.link(manipOutLeft.input)

def clamp(num, v0, v1):
    return max(v0, min(num, v1))

# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    # Output queues will be used to get the grayscale frames
    qRight = device.getOutputQueue(manipOutRight.getStreamName(), maxSize=4, blocking=False)
    qLeft = device.getOutputQueue(manipOutLeft.getStreamName(), maxSize=4, blocking=False)
    configQueue = device.getInputQueue(configIn.getStreamName())
    controlQueue = device.getInputQueue(controlIn.getStreamName())

    def displayFrame(name, frame):
        cv2.imshow(name, frame)

    sendCamConfig = False

    # Defaults and limits for manual focus/exposure controls
    expTime = 20000
    expMin = 1
    expMax = 33000

    sensIso = 800
    sensMin = 100
    sensMax = 1600

    while True:
        inRight = qRight.get()
        inLeft = qLeft.get()
        frameRight = inRight.getCvFrame()
        frameLeft = inLeft.getCvFrame()
        displayFrame("right", frameRight)
        displayFrame("left", frameLeft)

        # Update screen
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('c'):
            ctrl = dai.CameraControl()
            ctrl.setCaptureStill(True)
            controlQueue.send(ctrl)
        elif key == ord('e'):
            print("Autoexposure enable")
            ctrl = dai.CameraControl()
            ctrl.setAutoExposureEnable()
            controlQueue.send(ctrl)
        elif key in [ord('i'), ord('o'), ord('k'), ord('l')]:
            if key == ord('i'): expTime -= expStep
            if key == ord('o'): expTime += expStep
            if key == ord('k'): sensIso -= isoStep
            if key == ord('l'): sensIso += isoStep
            expTime = clamp(expTime, expMin, expMax)
            sensIso = clamp(sensIso, sensMin, sensMax)
            print("Setting manual exposure, time:", expTime, "iso:", sensIso)
            ctrl = dai.CameraControl()
            ctrl.setManualExposure(expTime, sensIso)
            controlQueue.send(ctrl)
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
            configQueue.send(cfg)
            sendCamConfig = False
