#!/usr/bin/env python3

from pathlib import Path
import sys
import cv2
import depthai as dai
import numpy as np
import time

'''
Mobilenet SSD device side decoding demo
  The "mobilenet-ssd" model is a Single-Shot multibox Detection (SSD) network intended
  to perform object detection. This model is implemented using the Caffe* framework.
  For details about this model, check out the repository <https://github.com/chuanqi305/MobileNet-SSD>.
'''

# MobilenetSSD label texts
labelMap = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
             "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

syncNN = True
flipRectified = True

# Get argument first
mobilenet_path = str((Path(__file__).parent / Path('models/mobilenet.blob')).resolve().absolute())
if len(sys.argv) > 1:
    mobilenet_path = sys.argv[1]

# Start defining a pipeline
pipeline = dai.Pipeline()


manip = pipeline.createImageManip()
manip.initialConfig.setResize(300, 300)
# The NN model expects BGR input. By default ImageManip output type would be same as input (gray in this case)
manip.initialConfig.setFrameType(dai.RawImgFrame.Type.BGR888p)
# manip.setKeepAspectRatio(False)

# Define a neural network that will make predictions based on the source frames
spatialDetectionNetwork = pipeline.createMobileNetSpatialDetectionNetwork()
spatialDetectionNetwork.setConfidenceThreshold(0.5)
spatialDetectionNetwork.setBlobPath(mobilenet_path)
spatialDetectionNetwork.input.setBlocking(False)
spatialDetectionNetwork.setBoundingBoxScaleFactor(0.5)
spatialDetectionNetwork.setDepthLowerThreshold(100)
spatialDetectionNetwork.setDepthUpperThreshold(5000)

manip.out.link(spatialDetectionNetwork.input)

# Create outputs
xoutManip = pipeline.createXLinkOut()
xoutManip.setStreamName("right")
if(syncNN):
    spatialDetectionNetwork.passthrough.link(xoutManip.input)
else:
    manip.out.link(xoutManip.input)

depthRoiMap = pipeline.createXLinkOut()
depthRoiMap.setStreamName("depthRoiMap")

xoutDepth = pipeline.createXLinkOut()
xoutDepth.setStreamName("depth")

xout_nn = pipeline.createXLinkOut()
xout_nn.setStreamName("detections")
spatialDetectionNetwork.out.link(xout_nn.input)
spatialDetectionNetwork.passthroughRoi.link(depthRoiMap.input)

monoLeft = pipeline.createMonoCamera()
monoRight = pipeline.createMonoCamera()
stereo = pipeline.createStereoDepth()
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
stereo.setOutputDepth(True)
stereo.setConfidenceThreshold(255)
stereo.setOutputRectified(True)

stereo.rectifiedRight.link(manip.inputImage)

monoLeft.out.link(stereo.left)
monoRight.out.link(stereo.right)

stereo.depth.link(spatialDetectionNetwork.inputDepth)
stereo.depth.link(xoutDepth.input)

# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    # Output queues will be used to get the rgb frames and nn data from the outputs defined above
    previewQueue = device.getOutputQueue(name="right", maxSize=4, blocking=False)
    detectionNNQueue = device.getOutputQueue(name="detections", maxSize=4, blocking=False)
    depthRoiMap = device.getOutputQueue(name="depthRoiMap", maxSize=4, blocking=False)
    depthQueue = device.getOutputQueue(name="depth", maxSize=4, blocking=False)

    rectifiedRight = None
    detections = []

    start_time = time.monotonic()
    counter = 0
    fps = 0
    color = (255, 255, 255)

    while True:
        inRectified = previewQueue.get()
        in_nn = detectionNNQueue.get()
        depth = depthQueue.get()

        counter+=1
        current_time = time.monotonic()
        if (current_time - start_time) > 1 :
            fps = counter / (current_time - start_time)
            counter = 0
            start_time = current_time
        
        rectifiedRight = inRectified.getCvFrame()

        depthFrame = depth.getFrame()

        depthFrameColor = cv2.normalize(depthFrame, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
        depthFrameColor = cv2.equalizeHist(depthFrameColor)
        depthFrameColor = cv2.applyColorMap(depthFrameColor, cv2.COLORMAP_HOT)
        detections = in_nn.detections
        if len(detections) != 0:
            passthroughRoi = depthRoiMap.get()
            roiDatas = passthroughRoi.getConfigData()

            for roiData in roiDatas:
                roi = roiData.roi
                xmin = int(roi.xmin * depth.getWidth())
                ymin = int(roi.ymin * depth.getHeight())
                xmax = int(roi.xmax * depth.getWidth())
                ymax = int(roi.ymax * depth.getHeight())
                cv2.rectangle(depthFrameColor, (xmin, ymin), (xmax, ymax), color, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX)

        if flipRectified:
            rectifiedRight = cv2.flip(rectifiedRight, 1)

        # if the rectifiedRight is available, draw bounding boxes on it and show the rectifiedRight
        height = rectifiedRight.shape[0]
        width  = rectifiedRight.shape[1]
        for detection in detections:
            if flipRectified:
                swap = detection.xmin
                detection.xmin = 1 - detection.xmax
                detection.xmax = 1 - swap
            #denormalize bounging box
            x1 = int(detection.xmin * width)
            x2 = int(detection.xmax * width)
            y1 = int(detection.ymin * height)
            y2 = int(detection.ymax * height)

            try:
                label = labelMap[detection.label]
            except:
                label = detection.label
            
            cv2.putText(rectifiedRight, str(label), (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
            cv2.putText(rectifiedRight, "{:.2f}".format(detection.confidence*100), (x1 + 10, y1 + 35), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
            cv2.putText(rectifiedRight, f"X: {int(detection.spatialCoordinates.x)}", (x1 + 10, y1 + 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
            cv2.putText(rectifiedRight, f"Y: {int(detection.spatialCoordinates.y)}", (x1 + 10, y1 + 65), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
            cv2.putText(rectifiedRight, f"Z: {int(detection.spatialCoordinates.z)}", (x1 + 10, y1 + 80), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)

            cv2.rectangle(rectifiedRight, (x1, y1), (x2, y2), color, cv2.FONT_HERSHEY_SIMPLEX)

        cv2.putText(rectifiedRight, "NN fps: {:.2f}".format(fps), (2, rectifiedRight.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.4, color)
        cv2.imshow("depth", depthFrameColor)
        cv2.imshow("rectified right", rectifiedRight)

        if cv2.waitKey(1) == ord('q'):
            break