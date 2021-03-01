#!/usr/bin/env python3

'''
Mono camera control demo:
  Control:      key[dec/inc]  min..max
  exposure time:     I   O      1..33000 [us]
  sensitivity iso:   K   L    100..1600
Back to autoexposure: 'E'
'''

import cv2
import depthai as dai
import numpy as np

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - two mono (grayscale) cameras
cam_left = pipeline.createMonoCamera()
cam_left.setBoardSocket(dai.CameraBoardSocket.LEFT)
cam_left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

cam_right = pipeline.createMonoCamera()
cam_right.setBoardSocket(dai.CameraBoardSocket.RIGHT)
cam_right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

# Create outputs
xout_left = pipeline.createXLinkOut()
xout_left.setStreamName('left')
cam_left.out.link(xout_left.input)
xout_right = pipeline.createXLinkOut()
xout_right.setStreamName('right')
cam_right.out.link(xout_right.input)

# Create and link control input
control_in = pipeline.createXLinkIn()
control_in.setStreamName('control')
control_in.out.link(cam_left.inputControl)
control_in.out.link(cam_right.inputControl)

def clamp(num, v0, v1): return max(v0, min(num, v1))

# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    # Output queues will be used to get the grayscale frames from the outputs defined above
    q_left = device.getOutputQueue(name="left", maxSize=4, blocking=False)
    q_right = device.getOutputQueue(name="right", maxSize=4, blocking=False)
    # Input queue for control commands
    controlQueue = device.getInputQueue('control')

    # Manual exposure: key-press step, defaults and limits
    EXP_STEP = 500  # us
    ISO_STEP = 50

    exp_time = 20000
    exp_min = 1
    exp_max = 33000

    sens_iso = 800
    sens_min = 100
    sens_max = 1600

    frame_left = None
    frame_right = None

    while True:
        # instead of get (blocking) used tryGet (nonblocking) which will return the available data or None otherwise
        in_left = q_left.tryGet()
        in_right = q_right.tryGet()

        if in_left is not None:
            # if the data from the left camera is available, transform the 1D data into a frame
            frame_left = in_left.getData().reshape((in_left.getHeight(), in_left.getWidth())).astype(np.uint8)
            frame_left = np.ascontiguousarray(frame_left)

        if in_right is not None:
            # if the data from the right camera is available, transform the 1D data into a frame
            frame_right = in_right.getData().reshape((in_right.getHeight(), in_right.getWidth())).astype(np.uint8)
            frame_right = np.ascontiguousarray(frame_right)

        # show the frames if available
        if frame_left is not None:
            cv2.imshow("left", frame_left)
        if frame_right is not None:
            cv2.imshow("right", frame_right)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key in [ord('i'), ord('o'), ord('k'), ord('l')]:
            if key == ord('i'): exp_time -= EXP_STEP
            if key == ord('o'): exp_time += EXP_STEP
            if key == ord('k'): sens_iso -= ISO_STEP
            if key == ord('l'): sens_iso += ISO_STEP
            exp_time = clamp(exp_time, exp_min, exp_max)
            sens_iso = clamp(sens_iso, sens_min, sens_max)
            print("Setting manual exposure, time:", exp_time, "iso:", sens_iso)
            ctrl = dai.CameraControl()
            ctrl.setManualExposure(exp_time, sens_iso)
            controlQueue.send(ctrl)
        elif key == ord('e'):
            print("Autoexposure enable")
            ctrl = dai.CameraControl()
            ctrl.setAutoExposureEnable()
            controlQueue.send(ctrl)
