#!/usr/bin/env python3

import blobconverter
import cv2
import depthai as dai
import numpy as np

pipeline = dai.Pipeline()

cam = pipeline.createColorCamera()
cam.setBoardSocket(dai.CameraBoardSocket.RGB)
cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
cam.setPreviewSize(300, 300)
cam.setInterleaved(False)

videoEncoder = pipeline.createVideoEncoder()
videoEncoder.setDefaultProfilePreset(1920, 1080, 30, dai.VideoEncoderProperties.Profile.H265_MAIN)
cam.video.link(videoEncoder.input)

nn = pipeline.createMobileNetDetectionNetwork()
nn.setConfidenceThreshold(0.5)
nn.setBlobPath(str(blobconverter.from_zoo("mobilenet-ssd", shaves=6)))
nn.setNumInferenceThreads(2)
nn.input.setBlocking(False)
cam.preview.link(nn.input)

videoOut = pipeline.createXLinkOut()
videoOut.setStreamName('h265')
videoEncoder.bitstream.link(videoOut.input)

xoutRgb = pipeline.createXLinkOut()
xoutRgb.setStreamName("rgb")
cam.preview.link(xoutRgb.input)

nnOut = pipeline.createXLinkOut()
nnOut.setStreamName("nn")
nn.out.link(nnOut.input)

# MobilenetSSD label texts
labelMap = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
            "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

with dai.Device(pipeline) as device, open('video.h265', 'wb') as videoFile:
    device.startPipeline()

    queue_size = 8
    qRgb = device.getOutputQueue("rgb", queue_size)
    qDet = device.getOutputQueue("nn", queue_size)
    qRgbEnc = device.getOutputQueue('h265', maxSize=30, blocking=True)

    frame = None
    detections = []


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
        inRgb = qRgb.tryGet()
        inDet = qDet.tryGet()

        while qRgbEnc.has():
            qRgbEnc.get().getData().tofile(videoFile)

        if inRgb is not None:
            frame = inRgb.getCvFrame()

        if inDet is not None:
            detections = inDet.detections

        if frame is not None:
            displayFrame("rgb", frame)

        if cv2.waitKey(1) == ord('q'):
            break

print("To view the encoded data, convert the stream file (.h265) into a video file (.mp4) using a command below:")
print("ffmpeg -framerate 30 -i video.h265 -c copy video.mp4")
