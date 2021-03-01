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

cam_right = pipeline.createMonoCamera()
cam_right.setBoardSocket(dai.CameraBoardSocket.RIGHT)
cam_right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

detection_nn = pipeline.createNeuralNetwork()
detection_nn.setBlobPath(mobilenet_path)

manip = pipeline.createImageManip()
manip.initialConfig.setResize(300, 300)
# The NN model expects BGR input. By default ImageManip output type would be same as input (gray in this case)
manip.initialConfig.setFrameType(dai.RawImgFrame.Type.BGR888p)
cam_right.out.link(manip.inputImage)
manip.out.link(detection_nn.input)

xout_right = pipeline.createXLinkOut()
xout_right.setStreamName("right")
cam_right.out.link(xout_right.input)

xout_manip = pipeline.createXLinkOut()
xout_manip.setStreamName("manip")
manip.out.link(xout_manip.input)

xout_nn = pipeline.createXLinkOut()
xout_nn.setStreamName("nn")
detection_nn.out.link(xout_nn.input)

# MobilenetSSD label texts
texts = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
         "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    queue_size = 8
    q_right = device.getOutputQueue("right", queue_size)
    q_manip = device.getOutputQueue("manip", queue_size)
    q_nn = device.getOutputQueue("nn", queue_size)
    q_rgb_enc = device.getOutputQueue('h265', maxSize=30, blocking=True)

    frame = None
    frame_manip = None
    bboxes = []
    confidences = []
    labels = []

    def frame_norm(frame, bbox):
        norm_vals = np.full(len(bbox), frame.shape[0])
        norm_vals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * norm_vals).astype(int)

    videoFile = open('video.h265','wb')

    while True:
        in_right = q_right.tryGet()
        in_manip = q_manip.tryGet()
        in_nn = q_nn.tryGet()

        while q_rgb_enc.has():
            q_rgb_enc.get().getData().tofile(videoFile)

        if in_right is not None:
            shape = (in_right.getHeight(), in_right.getWidth())
            frame = in_right.getData().reshape(shape).astype(np.uint8)
            frame = np.ascontiguousarray(frame)

        if in_manip is not None:
            shape = (3, in_manip.getHeight(), in_manip.getWidth())
            frame_manip = in_manip.getData().reshape(shape).transpose(1, 2, 0).astype(np.uint8)
            frame_manip = np.ascontiguousarray(frame_manip)

        if in_nn is not None:
            bboxes = np.array(in_nn.getFirstLayerFp16())
            bboxes = bboxes.reshape((bboxes.size // 7, 7))
            bboxes = bboxes[bboxes[:, 2] > 0.5]
            # Cut bboxes and labels
            labels = bboxes[:, 1].astype(int)
            confidences = bboxes[:, 2]
            bboxes = bboxes[:, 3:7]

        if frame is not None:
            for raw_bbox, label, conf in zip(bboxes, labels, confidences):
                bbox = frame_norm(frame, raw_bbox)
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
                cv2.putText(frame, texts[label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                cv2.putText(frame, f"{int(conf * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.imshow("right", frame)

        if frame_manip is not None:
            for raw_bbox, label, conf in zip(bboxes, labels, confidences):
                bbox = frame_norm(frame_manip, raw_bbox)
                cv2.rectangle(frame_manip, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
                cv2.putText(frame_manip, texts[label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                cv2.putText(frame_manip, f"{int(conf * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.imshow("manip", frame_manip)

        if cv2.waitKey(1) == ord('q'):
            break

    videoFile.close()

    print("To view the encoded data, convert the stream file (.h265) into a video file (.mp4) using a command below:")
    print("ffmpeg -framerate 30 -i video.h265 -c copy video.mp4")
