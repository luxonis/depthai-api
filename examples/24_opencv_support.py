#!/usr/bin/env python3

import cv2
import depthai as dai
import numpy as np

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - color camera
cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(300, 300)
cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
cam_rgb.setInterleaved(True)
cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

# Create output
xout_video = pipeline.createXLinkOut()
xout_video.setStreamName("video")
xout_preview = pipeline.createXLinkOut()
xout_preview.setStreamName("preview")

cam_rgb.preview.link(xout_preview.input)
cam_rgb.video.link(xout_video.input)

# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    while True:
        # Get preview and video frames
        preview = device.getOutputQueue('preview').get()
        video = device.getOutputQueue('video').get()

        # Show 'preview' frame as is (already in correct format, no copy is made)
        cv2.imshow("preview", preview.getFrame())
        # Get BGR frame from NV12 encoded video frame to show with opencv
        cv2.imshow("video", video.getCvFrame())

        if cv2.waitKey(1) == ord('q'):
            break
