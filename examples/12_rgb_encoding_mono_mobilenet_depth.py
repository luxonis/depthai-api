#!/usr/bin/env python3

from pathlib import Path
import sys

import blobconverter
import cv2
import depthai as dai
import numpy as np

flipRectified = True

pipeline = dai.Pipeline()

cam = pipeline.createColorCamera()
cam.setBoardSocket(dai.CameraBoardSocket.RGB)
cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)

videoEncoder = pipeline.createVideoEncoder()
videoEncoder.setDefaultProfilePreset(1920, 1080, 30, dai.VideoEncoderProperties.Profile.H265_MAIN)
cam.video.link(videoEncoder.input)

videoOut = pipeline.createXLinkOut()
videoOut.setStreamName('h265')
videoEncoder.bitstream.link(videoOut.input)
camLeft = pipeline.createMonoCamera()
camLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
camLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)

camRight = pipeline.createMonoCamera()
camRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
camRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)

depth = pipeline.createStereoDepth()
depth.setConfidenceThreshold(255)
# Note: the rectified streams are horizontally mirrored by default
depth.setOutputRectified(True)
depth.setRectifyMirrorFrame(False)
depth.setRectifyEdgeFillColor(0) # Black, to better see the cutout
camLeft.out.link(depth.left)
camRight.out.link(depth.right)
# Disparity range is 0..95, used for normalization
disparity_multiplier = 255 / 95

disparityOut = pipeline.createXLinkOut()
disparityOut.setStreamName("disparity")
depth.disparity.link(disparityOut.input)

nn = pipeline.createMobileNetDetectionNetwork()
nn.setConfidenceThreshold(0.5)
nn.setBlobPath(str(blobconverter.from_zoo("mobilenet-ssd", shaves=6)))
nn.setNumInferenceThreads(2)
nn.input.setBlocking(False)

manip = pipeline.createImageManip()
manip.initialConfig.setResize(300, 300)
# The NN model expects BGR input. By default ImageManip output type would be same as input (gray in this case)
manip.initialConfig.setFrameType(dai.RawImgFrame.Type.BGR888p)
depth.rectifiedRight.link(manip.inputImage)
manip.out.link(nn.input)

xoutRight = pipeline.createXLinkOut()
xoutRight.setStreamName("right")
camRight.out.link(xoutRight.input)

manipOut = pipeline.createXLinkOut()
manipOut.setStreamName("manip")
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

    queueSize = 8
    qRight = device.getOutputQueue("right", queueSize)
    qDisparity = device.getOutputQueue("disparity", queueSize)
    qManip = device.getOutputQueue("manip", queueSize)
    qDet = device.getOutputQueue("nn", queueSize)
    qRgbEnc = device.getOutputQueue('h265', maxSize=30, blocking=True)

    frame = None
    frameManip = None
    frameDisparity = None
    detections = []
    offsetX = (camRight.getResolutionWidth() - camRight.getResolutionHeight()) // 2
    croppedFrame = np.zeros((camRight.getResolutionHeight(), camRight.getResolutionHeight()))

    def frameNorm(frame, bbox):
        normVals = np.full(len(bbox), frame.shape[0])
        normVals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

    videoFile = open('video.h265', 'wb')
    cv2.namedWindow("right", cv2.WINDOW_NORMAL)
    cv2.namedWindow("manip", cv2.WINDOW_NORMAL)
    cv2.namedWindow("depth", cv2.WINDOW_NORMAL)

    while True:
        inRight = qRight.tryGet()
        inManip = qManip.tryGet()
        inDet = qDet.tryGet()
        inDisparity = qDisparity.tryGet()

        while qRgbEnc.has():
            qRgbEnc.get().getData().tofile(videoFile)

        if inRight is not None:
            frame = cv2.flip(inRight.getCvFrame(), 1)
            if flipRectified:
                frame = cv2.flip(frame, 1)

        if inManip is not None:
            frameManip = inManip.getCvFrame()

        if inDisparity is not None:
            # Flip disparity frame, normalize it and apply color map for better visualization
            frameDisparity = inDisparity.getFrame()
            if flipRectified:
                frameDisparity = cv2.flip(frameDisparity, 1)
            frameDisparity = (frameDisparity*disparity_multiplier).astype(np.uint8)
            frameDisparity = cv2.applyColorMap(frameDisparity, cv2.COLORMAP_JET)

        if inDet is not None:
            detections = inDet.detections

        if frame is not None:
            for detection in detections:
                bbox = frameNorm(croppedFrame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                bbox[::2] += offsetX
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
                cv2.putText(frame, labelMap[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                cv2.putText(frame, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.imshow("right", frame)

        if frameDisparity is not None:
            for detection in detections:
                bbox = frameNorm(croppedFrame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                bbox[::2] += offsetX
                cv2.rectangle(frameDisparity, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
                cv2.putText(frameDisparity, labelMap[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                cv2.putText(frameDisparity, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.imshow("disparity", frameDisparity)

        if frameManip is not None:
            for detection in detections:
                bbox = frameNorm(frameManip, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                cv2.rectangle(frameManip, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
                cv2.putText(frameManip, labelMap[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                cv2.putText(frameManip, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.imshow("manip", frameManip)

        if cv2.waitKey(1) == ord('q'):
            break

    videoFile.close()

    print("To view the encoded data, convert the stream file (.h265) into a video file (.mp4) using a command below:")
    print("ffmpeg -framerate 30 -i video.h265 -c copy video.mp4")
