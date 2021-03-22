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
if syncNN:
    spatialDetectionNetwork.passthrough.link(xoutManip.input)
else:
    manip.out.link(xoutManip.input)

depthRoiMap = pipeline.createXLinkOut()
depthRoiMap.setStreamName("boundingBoxDepthMapping")

xoutDepth = pipeline.createXLinkOut()
xoutDepth.setStreamName("depth")

xout_nn = pipeline.createXLinkOut()
xout_nn.setStreamName("detections")
spatialDetectionNetwork.out.link(xout_nn.input)
spatialDetectionNetwork.boundingBoxMapping.link(depthRoiMap.input)

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
spatialDetectionNetwork.passthroughDepth.link(xoutDepth.input)

# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    # Output queues will be used to get the rgb frames and nn data from the outputs defined above
    previewQueue = device.getOutputQueue(name="right", maxSize=4, blocking=False)
    detectionNNQueue = device.getOutputQueue(name="detections", maxSize=4, blocking=False)
    depthRoiMap = device.getOutputQueue(name="boundingBoxDepthMapping", maxSize=4, blocking=False)
    depthQueue = device.getOutputQueue(name="depth", maxSize=4, blocking=False)

    rectifiedRight = None
    detections = []
    start_time = time.monotonic()
    counter = 0
    color = (255, 255, 255)

    def frame_norm(frame, bbox):
        norm_vals = np.full(len(bbox), frame.shape[0])
        norm_vals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * norm_vals).astype(int)

    def display_frame(name, frame):
        for detection in detections:
            bbox = frame_norm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
            cv2.putText(frame, labelMap[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
            cv2.putText(frame, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
            cv2.putText(frame, f"X: {int(detection.spatialCoordinates.x)} mm", (bbox[0] + 10, bbox[1] + 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
            cv2.putText(frame, f"Y: {int(detection.spatialCoordinates.y)} mm", (bbox[0] + 10, bbox[1] + 65), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
            cv2.putText(frame, f"Z: {int(detection.spatialCoordinates.z)} mm", (bbox[0] + 10, bbox[1] + 80), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
        cv2.imshow(name, frame)

    while True:
        inRectified = previewQueue.get()
        in_nn = detectionNNQueue.get()
        depth = depthQueue.get()

        counter += 1
        
        rectifiedRight = inRectified.getCvFrame()
        if flipRectified:
            rectifiedRight = cv2.flip(rectifiedRight, 1)

        depthFrame = depth.getFrame()
        detections = in_nn.detections

        cv2.putText(rectifiedRight, "NN fps: {:.2f}".format(counter / (time.monotonic() - start_time)),
                    (2, rectifiedRight.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.4, color)

        depthFrameColor = cv2.normalize(depthFrame, None, 255, 0, cv2.NORM_INF, cv2.CV_8UC1)
        depthFrameColor = cv2.equalizeHist(depthFrameColor)
        depthFrameColor = cv2.applyColorMap(depthFrameColor, cv2.COLORMAP_HOT)

        if len(detections) != 0:
            boundingBoxMapping = depthRoiMap.get()
            roiDatas = boundingBoxMapping.getConfigData()

            for roiData in roiDatas:
                roi = roiData.roi
                roi = roi.denormalize(depthFrameColor.shape[1], depthFrameColor.shape[0])
                topLeft = roi.topLeft()
                bottomRight = roi.bottomRight()
                xmin = int(topLeft.x)
                ymin = int(topLeft.y)
                xmax = int(bottomRight.x)
                ymax = int(bottomRight.y)

                cv2.rectangle(depthFrameColor, (xmin, ymin), (xmax, ymax), color, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX)

        cv2.imshow("depth", depthFrameColor)

        display_frame("rectified right", rectifiedRight)

        if cv2.waitKey(1) == ord('q'):
            break
