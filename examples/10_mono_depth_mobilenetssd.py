#!/usr/bin/env python3

import blobconverter
import cv2
import depthai as dai
import numpy as np


flipRectified = True

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - mono (grayscale) cameras
left = pipeline.createMonoCamera()
left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
left.setBoardSocket(dai.CameraBoardSocket.LEFT)

right = pipeline.createMonoCamera()
right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
right.setBoardSocket(dai.CameraBoardSocket.RIGHT)

# Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
stereo = pipeline.createStereoDepth()
stereo.setOutputRectified(True)  # The rectified streams are horizontally mirrored by default
stereo.setConfidenceThreshold(255)
stereo.setRectifyEdgeFillColor(0)  # Black, to better see the cutout from rectification (black stripe on the edges)

left.out.link(stereo.left)
right.out.link(stereo.right)

# Create a node to convert the grayscale frame into the nn-acceptable form
manip = pipeline.createImageManip()
manip.initialConfig.setResize(300, 300)
# The NN model expects BGR input. By default ImageManip output type would be same as input (gray in this case)
manip.initialConfig.setFrameType(dai.ImgFrame.Type.BGR888p)
stereo.rectifiedRight.link(manip.inputImage)

# Define a neural network that will make predictions based on the source frames
nn = pipeline.createMobileNetDetectionNetwork()
nn.setConfidenceThreshold(0.5)
nn.setBlobPath(str(blobconverter.from_zoo("mobilenet-ssd", shaves=6)))
nn.setNumInferenceThreads(2)
nn.input.setBlocking(False)
manip.out.link(nn.input)

# Create outputs
disparityOut = pipeline.createXLinkOut()
disparityOut.setStreamName("disparity")
stereo.disparity.link(disparityOut.input)

xoutRight = pipeline.createXLinkOut()
xoutRight.setStreamName("rectifiedRight")
manip.out.link(xoutRight.input)

nnOut = pipeline.createXLinkOut()
nnOut.setStreamName("nn")
nn.out.link(nnOut.input)

# MobilenetSSD label nnLabels
labelMap = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
            "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# Pipeline is defined, now we can connect to the device
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    # Output queues will be used to get the grayscale / depth frames and nn data from the outputs defined above
    qRight = device.getOutputQueue("rectifiedRight", maxSize=4, blocking=False)
    qDisparity = device.getOutputQueue("disparity", maxSize=4, blocking=False)
    qDet = device.getOutputQueue("nn", maxSize=4, blocking=False)

    rightFrame = None
    depthFrame = None
    detections = []
    offsetX = (right.getResolutionWidth() - right.getResolutionHeight()) // 2
    croppedFrame = np.zeros((right.getResolutionHeight(), right.getResolutionHeight()))

    # nn data, being the bounding box locations, are in <0..1> range - they need to be normalized with frame width/height
    def frameNorm(frame, bbox):
        normVals = np.full(len(bbox), frame.shape[0])
        normVals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

    # Add bounding boxes and text to the frame and show it to the user
    def show(name, frame):
        for detection in detections:
            bbox = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
            cv2.putText(frame, labelMap[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.putText(frame, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
        # Show the frame
        cv2.imshow(name, frame)

    disparity_multiplier = 255 / 95 # Disparity range is 0..95
    while True:
        # Instead of get (blocking), we use tryGet (nonblocking) which will return the available data or None otherwise
        inRight = qRight.tryGet()
        inDet = qDet.tryGet()
        inDisparity = qDisparity.tryGet()

        if inRight is not None:
            rightFrame = inRight.getCvFrame()
            if flipRectified:
                rightFrame = cv2.flip(rightFrame, 1)


        if inDet is not None:
            detections = inDet.detections
            if flipRectified:
                for detection in detections:
                    swap = detection.xmin
                    detection.xmin = 1 - detection.xmax
                    detection.xmax = 1 - swap

        if inDisparity is not None:
            # Frame is transformed, normalized, and color map will be applied to highlight the depth info
            disparityFrame = inDisparity.getFrame()
            disparityFrame = (disparityFrame*disparity_multiplier).astype(np.uint8)
            # Available color maps: https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html
            disparityFrame = cv2.applyColorMap(disparityFrame, cv2.COLORMAP_JET)
            show("disparity", disparityFrame)

        if rightFrame is not None:
            show("rectified right", rightFrame)

        detections = []

        if cv2.waitKey(1) == ord('q'):
            break
