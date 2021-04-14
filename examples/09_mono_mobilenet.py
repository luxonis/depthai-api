#!/usr/bin/env python3

import blobconverter
import cv2
import depthai as dai
import numpy as np

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - mono (grayscale) camera
camRight = pipeline.createMonoCamera()
camRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
camRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

# Define a neural network that will make predictions based on the source frames
nn = pipeline.createMobileNetDetectionNetwork()
nn.setConfidenceThreshold(0.5)
nn.setBlobPath(str(blobconverter.from_zoo("mobilenet-ssd", shaves=6)))
nn.setNumInferenceThreads(2)
nn.input.setBlocking(False)

# Create a node to convert the grayscale frame into the nn-acceptable form
manip = pipeline.createImageManip()
manip.initialConfig.setResize(300, 300)
# The NN model expects BGR input. By default ImageManip output type would be same as input (gray in this case)
manip.initialConfig.setFrameType(dai.RawImgFrame.Type.BGR888p)
camRight.out.link(manip.inputImage)
manip.out.link(nn.input)

# Create outputs
manipOut = pipeline.createXLinkOut()
manipOut.setStreamName("right")
manip.out.link(manipOut.input)

nnOut = pipeline.createXLinkOut()
nnOut.setStreamName("nn")
nn.out.link(nnOut.input)

# MobilenetSSD label texts
labelMap = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
            "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# Pipeline is defined, now we can connect to the device
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    # Output queues will be used to get the grayscale frames and nn data from the outputs defined above
    qRight = device.getOutputQueue("right", maxSize=4, blocking=False)
    qDet = device.getOutputQueue("nn", maxSize=4, blocking=False)

    frame = None
    detections = []

    # nn data, being the bounding box locations, are in <0..1> range - they need to be normalized with frame width/height
    def frameNorm(frame, bbox):
        normVals = np.full(len(bbox), frame.shape[0])
        normVals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

    def displayFrame(name, frame):
        for detection in detections:
            bbox = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
            cv2.putText(frame, labelMap[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.putText(frame, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
        cv2.imshow(name, frame)


    while True:
        # Instead of get (blocking), we use tryGet (nonblocking) which will return the available data or None otherwise
        inRight = qRight.tryGet()
        inDet = qDet.tryGet()

        if inRight is not None:
            frame = inRight.getCvFrame()

        if inDet is not None:
            detections = inDet.detections

        if frame is not None:
            displayFrame("right", frame)

        if cv2.waitKey(1) == ord('q'):
            break
