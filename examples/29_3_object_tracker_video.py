#!/usr/bin/env python3

from pathlib import Path

import blobconverter
import cv2
import depthai as dai
import numpy as np
import time
import argparse

labelMap = ["person", ""]

videoPathDefault = str((Path(__file__).parent / Path('construction_vest.mp4')).resolve().absolute())
parser = argparse.ArgumentParser()
parser.add_argument('-vid', '--videoPath', help="Path to video frame", default=videoPathDefault)

args = parser.parse_args()

# Start defining a pipeline
pipeline = dai.Pipeline()

# Create neural network input
xinFrame = pipeline.createXLinkIn()
xinFrame.setStreamName("inFrame")
xinFrame.setMaxDataSize(1920*1080*3)

detectionNetwork = pipeline.createMobileNetDetectionNetwork()
objectTracker = pipeline.createObjectTracker()
trackerOut = pipeline.createXLinkOut()

xlinkOut = pipeline.createXLinkOut()

xlinkOut.setStreamName("trackerFrame")
trackerOut.setStreamName("tracklets")

# Create a node to convert the grayscale frame into the nn-acceptable form
manip = pipeline.createImageManip()
manip.initialConfig.setResizeThumbnail(384, 384)
# manip.initialConfig.setResize(384, 384)
# manip.initialConfig.setKeepAspectRatio(False) #squash the image to not lose FOV
# The NN model expects BGR input. By default ImageManip output type would be same as input (gray in this case)
manip.initialConfig.setFrameType(dai.ImgFrame.Type.BGR888p)
xinFrame.out.link(manip.inputImage)
manip.inputImage.setBlocking(True)

manipOut = pipeline.createXLinkOut()
manipOut.setStreamName("manip")
manip.out.link(manipOut.input)

nnOut = pipeline.createXLinkOut()
nnOut.setStreamName("nn")
detectionNetwork.out.link(nnOut.input)


# setting node configs
detectionNetwork.setBlobPath(str(blobconverter.from_zoo("person-detection-0201", shaves=7)))
detectionNetwork.setConfidenceThreshold(0.5)

manip.out.link(detectionNetwork.input)
detectionNetwork.input.setBlocking(True)
objectTracker.passthroughTrackerFrame.link(xlinkOut.input)


objectTracker.setDetectionLabelsToTrack([0])  # track only person
# possible tracking types: ZERO_TERM_COLOR_HISTOGRAM, ZERO_TERM_IMAGELESS
objectTracker.setTrackerType(dai.TrackerType.ZERO_TERM_COLOR_HISTOGRAM)
# take the smallest ID when new object is tracked, possible options: SMALLEST_ID, UNIQUE_ID
objectTracker.setTrackerIdAssigmentPolicy(dai.TrackerIdAssigmentPolicy.SMALLEST_ID)

xinFrame.out.link(objectTracker.inputTrackerFrame)
objectTracker.inputTrackerFrame.setBlocking(True)
detectionNetwork.passthrough.link(objectTracker.inputDetectionFrame)
objectTracker.inputDetectionFrame.setBlocking(True)
detectionNetwork.out.link(objectTracker.inputDetections)
objectTracker.inputDetections.setBlocking(True)
objectTracker.out.link(trackerOut.input)


# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:

    # Start the pipeline
    device.startPipeline()

    qIn = device.getInputQueue(name="inFrame")
    trackerFrameQ = device.getOutputQueue("trackerFrame", 4)
    tracklets = device.getOutputQueue("tracklets", 4)
    qManip = device.getOutputQueue("manip", maxSize=4)
    qDet = device.getOutputQueue("nn", maxSize=4)

    startTime = time.monotonic()
    counter = 0
    fps = 0
    detections = []
    frame = None

    def to_planar(arr: np.ndarray, shape: tuple) -> np.ndarray:
        return cv2.resize(arr, shape).transpose(2, 0, 1).flatten()

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

    cap = cv2.VideoCapture(args.videoPath)
    baseTs = time.monotonic()
    simulatedFps = 30
    inputFrameShape = (1280, 720)

    while cap.isOpened():
        read_correctly, frame = cap.read()
        if not read_correctly:
            break

        img = dai.ImgFrame()
        img.setType(dai.ImgFrame.Type.BGR888p)
        img.setData(to_planar(frame, inputFrameShape))
        img.setTimestamp(baseTs)
        baseTs += 1/simulatedFps

        img.setWidth(inputFrameShape[0])
        img.setHeight(inputFrameShape[1])
        qIn.send(img)

        trackFrame = trackerFrameQ.tryGet()
        if trackFrame is None:
            continue

        track = tracklets.get()
        manip = qManip.get()
        inDet = qDet.get()

        counter+=1
        current_time = time.monotonic()
        if (current_time - startTime) > 1 :
            fps = counter / (current_time - startTime)
            counter = 0
            startTime = current_time

        detections = inDet.detections
        manipFrame = manip.getCvFrame()
        displayFrame("nn", manipFrame)

        color = (255, 0, 0)
        trackerFrame = trackFrame.getCvFrame()
        trackletsData = track.tracklets
        for t in trackletsData:
            roi = t.roi.denormalize(trackerFrame.shape[1], trackerFrame.shape[0])
            x1 = int(roi.topLeft().x)
            y1 = int(roi.topLeft().y)
            x2 = int(roi.bottomRight().x)
            y2 = int(roi.bottomRight().y)

            try:
                label = labelMap[t.label]
            except:
                label = t.label

            statusMap = {dai.Tracklet.TrackingStatus.NEW : "NEW", dai.Tracklet.TrackingStatus.TRACKED : "TRACKED", dai.Tracklet.TrackingStatus.LOST : "LOST"}
            cv2.putText(trackerFrame, str(label), (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
            cv2.putText(trackerFrame, f"ID: {[t.id]}", (x1 + 10, y1 + 35), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
            cv2.putText(trackerFrame, statusMap[t.status], (x1 + 10, y1 + 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
            cv2.rectangle(trackerFrame, (x1, y1), (x2, y2), color, cv2.FONT_HERSHEY_SIMPLEX)

        cv2.putText(trackerFrame, "Fps: {:.2f}".format(fps), (2, trackerFrame.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.4, color)

        cv2.imshow("tracker", trackerFrame)

        if cv2.waitKey(1) == ord('q'):
            break
