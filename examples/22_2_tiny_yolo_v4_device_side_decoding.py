#!/usr/bin/env python3

from pathlib import Path
import sys
import cv2
import depthai as dai
import numpy as np
import time

'''
Tiny-yolo-v4 device side decoding demo
  The code is the same as for Tiny-yolo-V3, the only difference is the blob file.
  The blob was compiled following this tutorial: https://github.com/TNTWEN/OpenVINO-YOLOV4
'''

# tiny yolo v4 label texts
label_map = ["person",         "bicycle",    "car",           "motorbike",     "aeroplane",   "bus",           "train",
             "truck",          "boat",       "traffic light", "fire hydrant",  "stop sign",   "parking meter", "bench",
             "bird",           "cat",        "dog",           "horse",         "sheep",       "cow",           "elephant",
             "bear",           "zebra",      "giraffe",       "backpack",      "umbrella",    "handbag",       "tie",
             "suitcase",       "frisbee",    "skis",          "snowboard",     "sports ball", "kite",          "baseball bat",
             "baseball glove", "skateboard", "surfboard",     "tennis racket", "bottle",      "wine glass",    "cup",
             "fork",           "knife",      "spoon",         "bowl",          "banana",      "apple",         "sandwich",
             "orange",         "broccoli",   "carrot",        "hot dog",       "pizza",       "donut",         "cake",
             "chair",          "sofa",       "pottedplant",   "bed",           "diningtable", "toilet",        "tvmonitor",
             "laptop",         "mouse",      "remote",        "keyboard",      "cell phone",  "microwave",     "oven",
             "toaster",        "sink",       "refrigerator",  "book",          "clock",       "vase",          "scissors",
             "teddy bear",     "hair drier", "toothbrush"]  


syncNN = True

# Get argument first
tiny_yolo_v4_path = str((Path(__file__).parent / Path('models/tiny_yolo_v4_6shaves.blob')).resolve().absolute())
if len(sys.argv) > 1:
    tiny_yolo_v4_path = sys.argv[1]

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - color camera
cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(416, 416)
cam_rgb.setInterleaved(False)
cam_rgb.setFps(40)

#network specific settings
detectionNetwork = pipeline.createYoloDetectionNetwork()
detectionNetwork.setConfidenceThreshold(0.5)
detectionNetwork.setNumClasses(80)
detectionNetwork.setCoordinateSize(4)
anchors = np.array([10,14, 23,27, 37,58, 81,82, 135,169, 344,319])
detectionNetwork.setAnchors(anchors)
anchorMasks26 = np.array([1,2,3])
anchorMasks13 = np.array([3,4,5])
anchorMasks = {
    "side26": anchorMasks26,
    "side13": anchorMasks13,
}
detectionNetwork.setAnchorMasks(anchorMasks)
detectionNetwork.setIouThreshold(0.5)

detectionNetwork.setBlobPath(tiny_yolo_v4_path)
detectionNetwork.setNumInferenceThreads(2)
detectionNetwork.input.setBlocking(False)

cam_rgb.preview.link(detectionNetwork.input)

# Create outputs
xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("rgb")
if(syncNN):
    detectionNetwork.passthrough.link(xout_rgb.input)
else:
    cam_rgb.preview.link(xout_rgb.input)

xout_nn = pipeline.createXLinkOut()
xout_nn.setStreamName("detections")
detectionNetwork.out.link(xout_nn.input)


# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    # Output queues will be used to get the rgb frames and nn data from the outputs defined above
    q_rgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    q_nn = device.getOutputQueue(name="detections", maxSize=4, blocking=False)

    frame = None
    bboxes = []

    start_time = time.time()
    counter = 0
    fps = 0
    while True:
        if(syncNN):
            in_rgb = q_rgb.get()
            in_nn = q_nn.get()
        else:
            in_rgb = q_rgb.tryGet()
            in_nn = q_nn.tryGet()

        if in_rgb is not None:
            # if the data from the rgb camera is available, transform the 1D data into a HxWxC frame
            shape = (3, in_rgb.getHeight(), in_rgb.getWidth())
            frame = in_rgb.getData().reshape(shape).transpose(1, 2, 0).astype(np.uint8)
            frame = np.ascontiguousarray(frame)

        if in_nn is not None:
            bboxes = in_nn.detections
            counter+=1
            current_time = time.time()
            if (current_time - start_time) > 1 :
                fps = counter / (current_time - start_time)
                counter = 0
                start_time = current_time

        color = (255, 255, 255)

        if frame is not None:
            # if the frame is available, draw bounding boxes on it and show the frame
            height = frame.shape[0]
            width  = frame.shape[1]
            for bbox in bboxes:
                #denormalize bounging box
                x1 = int(bbox.xmin * width)
                x2 = int(bbox.xmax * width)
                y1 = int(bbox.ymin * height)
                y2 = int(bbox.ymax * height)
                try:
                    label = label_map[bbox.label]
                except:
                    label = bbox.label
                cv2.putText(frame, str(label), (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
                cv2.putText(frame, "{:.2f}".format(bbox.confidence*100), (x1 + 10, y1 + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, cv2.FONT_HERSHEY_SIMPLEX)

            cv2.putText(frame, "NN fps: {:.2f}".format(fps), (2, frame.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.4, color)
            cv2.imshow("rgb", frame)

        if cv2.waitKey(1) == ord('q'):
            break
