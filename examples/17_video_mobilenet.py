#!/usr/bin/env python3

from pathlib import Path
import sys
import cv2
import depthai as dai
import numpy as np
from time import monotonic

# Get argument first
mobilenet_path = str((Path(__file__).parent / Path('models/mobilenet.blob')).resolve().absolute())
video_path = str(Path("./construction_vest.mp4").resolve().absolute())
if len(sys.argv) > 2:
    mobilenet_path = sys.argv[1]
    video_path = sys.argv[2]

# Start defining a pipeline
pipeline = dai.Pipeline()


# Create neural network input
xin_nn = pipeline.createXLinkIn()
xin_nn.setStreamName("in_nn")

# Define a neural network that will make predictions based on the source frames
detection_nn = pipeline.createNeuralNetwork()
detection_nn.setBlobPath(mobilenet_path)
xin_nn.out.link(detection_nn.input)

# Create output
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
        
    # Output queues will be used to get the rgb frames and nn data from the outputs defined above
    q_in = device.getInputQueue(name="in_nn")
    q_nn = device.getOutputQueue(name="nn", maxSize=4, blocking=False)

    frame = None
    bboxes = []
    labels = []
    confidences = []

    # nn data, being the bounding box locations, are in <0..1> range - they need to be normalized with frame width/height
    def frame_norm(frame, bbox):
        norm_vals = np.full(len(bbox), frame.shape[0])
        norm_vals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * norm_vals).astype(int)


    def to_planar(arr: np.ndarray, shape: tuple) -> np.ndarray:
        return cv2.resize(arr, shape).transpose(2,0,1).flatten()

    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        read_correctly, frame = cap.read()
        if not read_correctly:
            break

        tstamp = monotonic()
        data = to_planar(frame, (300, 300))
        img = dai.ImgFrame()
        img.setData(data)
        img.setTimestamp(tstamp)
        img.setWidth(300)
        img.setHeight(300)
        q_in.send(img)


        in_nn = q_nn.tryGet()

        if in_nn is not None:
            # one detection has 7 numbers, and the last detection is followed by -1 digit, which later is filled with 0
            bboxes = np.array(in_nn.getFirstLayerFp16())
            # transform the 1D array into Nx7 matrix
            bboxes = bboxes.reshape((bboxes.size // 7, 7))
            # filter out the results which confidence less than a defined threshold
            bboxes = bboxes[bboxes[:, 2] > 0.5]
            # Cut bboxes and labels
            labels = bboxes[:, 1].astype(int)
            confidences = bboxes[:, 2]
            bboxes = bboxes[:, 3:7]

        if frame is not None:
            # if the frame is available, draw bounding boxes on it and show the frame
            for raw_bbox, label, conf in zip(bboxes, labels, confidences):
                bbox = frame_norm(frame, raw_bbox)
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
                cv2.putText(frame, texts[label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                cv2.putText(frame, f"{int(conf * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.imshow("rgb", frame)

        if cv2.waitKey(1) == ord('q'):
            break
