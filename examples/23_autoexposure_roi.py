#!/usr/bin/env python3

import blobconverter
import cv2
import depthai as dai
import numpy as np

# Press WASD to move a manual ROI window for auto-exposure control.
# Press N to go back to the region controlled by the NN detections.

previewSize = (300, 300)

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - color camera
camRgb = pipeline.createColorCamera()
camRgb.setPreviewSize(*previewSize)
camRgb.setInterleaved(False)

camControlIn = pipeline.createXLinkIn()
camControlIn.setStreamName('camControl')
camControlIn.out.link(camRgb.inputControl)

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
camRgb.preview.link(xoutRgb.input)

nnOut = pipeline.createXLinkOut()
nnOut.setStreamName("nn")
nn.out.link(nnOut.input)

# MobilenetSSD label texts
labelMap = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
            "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


def clamp(num, v0, v1):
    return max(v0, min(num, v1))


def asControl(roi):
    camControl = dai.CameraControl()
    camControl.setAutoExposureRegion(*roi)
    return camControl


class AutoExposureRegion:
    step = 10
    position = (0, 0)
    size = (100, 100)
    resolution = camRgb.getResolutionSize()
    maxDims = previewSize[0], previewSize[1]

    def grow(self, x=0, y=0):
        self.size = (
            clamp(x + self.size[0], 1, self.maxDims[0]),
            clamp(y + self.size[1], 1, self.maxDims[1])
        )

    def move(self, x=0, y=0):
        self.position = (
            clamp(x + self.position[0], 0, self.maxDims[0]),
            clamp(y + self.position[1], 0, self.maxDims[1])
        )

    def endPosition(self):
        return (
            clamp(self.position[0] + self.size[0], 0, self.maxDims[0]),
            clamp(self.position[1] + self.size[1], 0, self.maxDims[1]),
        )

    def toRoi(self):
        roi = np.array([*self.position, *self.size])
        # Convert to absolute camera coordinates
        roi = roi * self.resolution[1] // 300
        roi[0] += (self.resolution[0] - self.resolution[1]) // 2  # x offset for device crop
        return roi

    @staticmethod
    def bboxToRoi(bbox):
        startX, startY = bbox[:2]
        width, height = bbox[2] - startX, bbox[3] - startY
        roi = frameNorm(np.empty(camRgb.getResolutionSize()), (startX, startY, width, height))
        return roi


# Pipeline is defined, now we can connect to the device
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    # Output queues will be used to get the rgb frames and nn data from the outputs defined above
    qControl = device.getInputQueue(name="camControl")
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    qDet = device.getOutputQueue(name="nn", maxSize=4, blocking=False)
    frame = None
    detections = []

    nnRegion = True
    region = AutoExposureRegion()

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
        if not nnRegion:
            cv2.rectangle(frame, region.position, region.endPosition(), (0, 255, 0), 2)
        cv2.imshow(name, frame)

    while True:
        # Instead of get (blocking), we use tryGet (nonblocking) which will return the available data or None otherwise
        inRgb = qRgb.tryGet()
        inDet = qDet.tryGet()

        if inRgb is not None:
            frame = inRgb.getCvFrame()

        if inDet is not None:
            detections = inDet.detections

            if nnRegion and len(detections) > 0:
                bbox = (detections[0].xmin, detections[0].ymin, detections[0].xmax, detections[0].ymax)
                qControl.send(asControl(AutoExposureRegion.bboxToRoi(bbox)))

        if frame is not None:
            displayFrame("rgb", frame)

        key = cv2.waitKey(1)
        if key == ord('n'):
            print("AE ROI controlled by NN")
            nnRegion = True
        elif key in [ord('w'), ord('a'), ord('s'), ord('d'), ord('+'), ord('-')]:
            nnRegion = False
            if key == ord('a'):
                region.move(x=-region.step)
            if key == ord('d'):
                region.move(x=region.step)
            if key == ord('w'):
                region.move(y=-region.step)
            if key == ord('s'):
                region.move(y=region.step)
            if key == ord('+'):
                region.grow(x=10, y=10)
                region.step = region.step + 1
            if key == ord('-'):
                region.grow(x=-10, y=-10)
                region.step = max(region.step - 1, 1)
            print(f"Setting static AE ROI: {region.toRoi()} (on frame: {[*region.position, *region.endPosition()]})")
            qControl.send(asControl(region.toRoi()))
        elif key == ord('q'):
            break
