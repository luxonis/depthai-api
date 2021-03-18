#!/usr/bin/env python3

from pathlib import Path
import sys
import cv2
import depthai as dai
import numpy as np


# Get argument first
mobilenet_path = str((Path(__file__).parent / Path('models/mobilenet.blob')).resolve().absolute())
if len(sys.argv) > 1:
    mobilenet_path = sys.argv[1]

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

left = pipeline.createMonoCamera()
left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
left.setBoardSocket(dai.CameraBoardSocket.LEFT)

right = pipeline.createMonoCamera()
right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
right.setBoardSocket(dai.CameraBoardSocket.RIGHT)

depth = pipeline.createStereoDepth()
depth.setConfidenceThreshold(200)
# Note: the rectified streams are horizontally mirrored by default
depth.setOutputRectified(True)
depth.setRectifyEdgeFillColor(0) # Black, to better see the cutout
left.out.link(depth.left)
right.out.link(depth.right)

detection_nn = pipeline.createMobileNetDetectionNetwork()
detection_nn.setConfidenceThreshold(0.5)
detection_nn.setBlobPath(mobilenet_path)
detection_nn.setNumInferenceThreads(2)
detection_nn.input.setBlocking(False)

xout_depth = pipeline.createXLinkOut()
xout_depth.setStreamName("depth")
depth.disparity.link(xout_depth.input)

xout_right = pipeline.createXLinkOut()
xout_right.setStreamName("rect_right")
depth.rectifiedRight.link(xout_right.input)

manip = pipeline.createImageManip()
manip.initialConfig.setResize(300, 300)
# The NN model expects BGR input. By default ImageManip output type would be same as input (gray in this case)
manip.initialConfig.setFrameType(dai.RawImgFrame.Type.BGR888p)
depth.rectifiedRight.link(manip.inputImage)
manip.out.link(detection_nn.input)

xout_manip = pipeline.createXLinkOut()
xout_manip.setStreamName("manip")
manip.out.link(xout_manip.input)

xout_nn = pipeline.createXLinkOut()
xout_nn.setStreamName("nn")
detection_nn.out.link(xout_nn.input)

# MobilenetSSD label texts
nn_labels = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
             "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    q_right = device.getOutputQueue(name="rect_right", maxSize=8, blocking=False)
    q_manip = device.getOutputQueue(name="manip", maxSize=8, blocking=False)
    q_depth = device.getOutputQueue(name="depth", maxSize=8, blocking=False)
    q_nn = device.getOutputQueue(name="nn", maxSize=8, blocking=False)
    q_rgb_enc = device.getOutputQueue(name="h265", maxSize=30, blocking=True)

    frame_right = None
    frame_manip = None
    frame_depth = None
    detections = []


    def frame_norm(frame, bbox):
        norm_vals = np.full(len(bbox), frame.shape[0])
        norm_vals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * norm_vals).astype(int)

    def display_frame(name, frame):
        for detection in detections:
            bbox = frame_norm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
            cv2.putText(frame, nn_labels[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.putText(frame, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
        cv2.imshow(name, frame)

    videoFile = open('video.h265', 'wb')

    while True:
        in_right = q_right.tryGet()
        in_manip = q_manip.tryGet()
        in_nn = q_nn.tryGet()
        in_depth = q_depth.tryGet()

        while q_rgb_enc.has():
            q_rgb_enc.get().getData().tofile(videoFile)

        if in_right is not None:
            frame_right = in_right.getCvFrame()

        if in_manip is not None:
            frame_manip = in_manip.getCvFrame()

        if in_nn is not None:
            detections = in_nn.detections

        if in_depth is not None:
            frame_depth = in_depth.getData().reshape((in_depth.getHeight(), in_depth.getWidth())).astype(np.uint8)
            frame_depth = np.ascontiguousarray(frame_depth)
            frame_depth = cv2.applyColorMap(frame_depth, cv2.COLORMAP_JET)

        if frame_right is not None:
            display_frame("rectif_right", frame_right)

        if frame_manip is not None:
            display_frame("manip", frame_manip)

        if frame_depth is not None:
            display_frame("depth", frame_depth)

        if cv2.waitKey(1) == ord('q'):
            break

    videoFile.close()

    print("To view the encoded data, convert the stream file (.h265) into a video file (.mp4) using a command below:")
    print("ffmpeg -framerate 30 -i video.h265 -c copy video.mp4")
