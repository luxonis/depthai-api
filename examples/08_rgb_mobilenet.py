#!/usr/bin/env python3

import cv2
import depthai as dai
import numpy as np
import time
import argparse
import blobconverter

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sync', action="store_true", help="Sync RGB output with NN output", default=False)
args = parser.parse_args()

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - color camera
camRgb = pipeline.createColorCamera()
camRgb.setPreviewSize(300, 300)
camRgb.setInterleaved(False)
camRgb.setFps(40)

# Define a neural network that will make predictions based on the source frames
nn = pipeline.createMobileNetDetectionNetwork()
nn.setConfidenceThreshold(0.5)
nn.setBlobPath(str(blobconverter.from_zoo("mobilenet-ssd", shaves=6)))
nn.setNumInferenceThreads(2)
nn.input.setBlocking(False)
camRgb.preview.link(nn.input)

# Create outputs
xoutRgb = pipeline.createXLinkOut()
xoutRgb.setStreamName("rgb")
if args.sync:
    nn.passthrough.link(xoutRgb.input)
else:
    camRgb.preview.link(xoutRgb.input)

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

    # Output queues will be used to get the rgb frames and nn data from the outputs defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    qDet = device.getOutputQueue(name="nn", maxSize=4, blocking=False)

    startTime = time.monotonic()
    counter = 0
    detections = []
    frame = None

    # nn data (bounding box locations) are in <0..1> range - they need to be normalized with frame width/height
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
        if args.sync:
            # Use blocking get() call to catch frame and inference result synced
            inRgb = qRgb.get()
            inDet = qDet.get()
        else:
            # Instead of get (blocking), we use tryGet (nonblocking) which will return the available data or None otherwise
            inRgb = qRgb.tryGet()
            inDet = qDet.tryGet()

        if inRgb is not None:
            frame = inRgb.getCvFrame()
            cv2.putText(frame, "NN fps: {:.2f}".format(counter / (time.monotonic() - startTime)),
                        (2, frame.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.4, color=(255, 255, 255))

        if inDet is not None:
            detections = inDet.detections
            counter += 1

        # If the frame is available, draw bounding boxes on it and show the frame
        if frame is not None:
            displayFrame("rgb", frame)

        if cv2.waitKey(1) == ord('q'):
            break
