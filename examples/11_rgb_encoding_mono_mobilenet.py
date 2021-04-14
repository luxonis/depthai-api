#!/usr/bin/env python3

import blobconverter
import cv2
import depthai as dai
import numpy as np

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

camRight = pipeline.createMonoCamera()
camRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
camRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

nn = pipeline.createMobileNetDetectionNetwork()
nn.setConfidenceThreshold(0.5)
nn.setBlobPath(str(blobconverter.from_zoo("mobilenet-ssd", shaves=6)))
nn.setNumInferenceThreads(2)
nn.input.setBlocking(False)

manip = pipeline.createImageManip()
manip.initialConfig.setResize(300, 300)
# The NN model expects BGR input. By default ImageManip output type would be same as input (gray in this case)
manip.initialConfig.setFrameType(dai.RawImgFrame.Type.BGR888p)
camRight.out.link(manip.inputImage)
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

    queue_size = 8
    qRight = device.getOutputQueue("right", queue_size)
    qManip = device.getOutputQueue("manip", queue_size)
    qDet = device.getOutputQueue("nn", queue_size)
    qRgbEnc = device.getOutputQueue('h265', maxSize=30, blocking=True)

    frame = None
    frameManip = None
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

    while True:
        inRight = qRight.tryGet()
        inManip = qManip.tryGet()
        inDet = qDet.tryGet()

        while qRgbEnc.has():
            qRgbEnc.get().getData().tofile(videoFile)

        if inRight is not None:
            frame = inRight.getCvFrame()

        if inManip is not None:
            frameManip = inManip.getCvFrame()

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
