#!/usr/bin/env python3

from pathlib import Path
import sys
import cv2
import depthai as dai
import numpy as np

# Get argument first
nnPath = str((Path(__file__).parent / Path('models/mobilenet-ssd_openvino_2021.2_6shave.blob')).resolve().absolute())
if len(sys.argv) > 1:
    nnPath = sys.argv[1]

if not Path(nnPath).exists():
    import sys
    raise FileNotFoundError(f'Required file/s not found, please run "{sys.executable} install_requirements.py"')

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - mono (grayscale) cameras
left = pipeline.createMonoCamera()
left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
left.setBoardSocket(dai.CameraBoardSocket.LEFT)

right = pipeline.createMonoCamera()
right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
right.setBoardSocket(dai.CameraBoardSocket.RIGHT)

# Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
stereo = pipeline.createStereoDepth()
# The rectified streams are horizontally mirrored by default
stereo.setConfidenceThreshold(255)
stereo.setRectifyEdgeFillColor(0)  # Black, to better see the cutout from rectification (black stripe on the edges)

left.out.link(stereo.left)
right.out.link(stereo.right)

# Create a node to convert the grayscale frame into the nn-acceptable form
manip = pipeline.createImageManip()
manip.initialConfig.setResize(300, 300)
# The NN model expects BGR input. By default ImageManip output type would be same as input (gray in this case)
manip.initialConfig.setFrameType(dai.RawImgFrame.Type.BGR888p)
stereo.rectifiedRight.link(manip.inputImage)

# Define a neural network that will make predictions based on the source frames
nn = pipeline.createMobileNetDetectionNetwork()
nn.setConfidenceThreshold(0.5)
nn.setBlobPath(nnPath)
nn.setNumInferenceThreads(2)
nn.input.setBlocking(False)
manip.out.link(nn.input)

# Create outputs
depthOut = pipeline.createXLinkOut()
depthOut.setStreamName("depth")

stereo.disparity.link(depthOut.input)

xoutRight = pipeline.createXLinkOut()
xoutRight.setStreamName("rectifiedRight")
manip.out.link(xoutRight.input)

nnOut = pipeline.createXLinkOut()
nnOut.setStreamName("nn")
nn.out.link(nnOut.input)

# MobilenetSSD label nnLabels
labelMap = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
            "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    # Output queues will be used to get the grayscale / depth frames and nn data from the outputs defined above
    qRight = device.getOutputQueue("rectifiedRight", maxSize=4, blocking=False)
    qDepth = device.getOutputQueue("depth", maxSize=4, blocking=False)
    qDet = device.getOutputQueue("nn", maxSize=4, blocking=False)

    rightFrame = None
    depthFrame = None
    detections = []
    offsetX = (right.getResolutionWidth() - right.getResolutionHeight()) // 2
    croppedFrame = np.zeros((right.getResolutionHeight(), right.getResolutionHeight()))

    # nn data, being the bounding box locations, are in <0..1> range - they need to be normalized with frame width/height
    def frameNorm(frame, bbox):
        normVals = np.full(len(bbox), frame.shape[0])
        normVals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

    while True:
        # instead of get (blocking) used tryGet (nonblocking) which will return the available data or None otherwise
        inRight = qRight.tryGet()
        inDet = qDet.tryGet()
        inDepth = qDepth.tryGet()

        if inRight is not None:
            rightFrame = inRight.getCvFrame()

        if inDet is not None:
            detections = inDet.detections

        if inDepth is not None:
            depthFrame = cv2.flip(inDepth.getFrame(), 1)
            # frame is transformed, the color map will be applied to highlight the depth info
            depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_JET)

            # Uncomment one of these and comment the one given above
            # to see visualisation in different color frames

            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_BONE)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_AUTUMN)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_WINTER)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_RAINBOW)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_OCEAN)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_SUMMER)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_SPRING)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_COOL)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_HSV)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_HOT)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_PINK)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_PARULA)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_MAGMA)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_INFERNO)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_PLASMA)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_VIRIDIS)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_CIVIDIS)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_TWILIGHT)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_TWILIGHT_SHIFTED)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_TURBO)
            # depthFrame = cv2.applyColorMap(depthFrame, cv2.COLORMAP_DEEPGREEN)

        if rightFrame is not None:
            for detection in detections:
                bbox = frameNorm(rightFrame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                cv2.rectangle(rightFrame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
                cv2.putText(rightFrame, labelMap[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                cv2.putText(rightFrame, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.imshow("rectified right", rightFrame)

        if depthFrame is not None:
            for detection in detections:
                bbox = frameNorm(croppedFrame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                bbox[::2] += offsetX
                cv2.rectangle(depthFrame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
                cv2.putText(depthFrame, labelMap[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                cv2.putText(depthFrame, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            cv2.imshow("depth", depthFrame)

        if cv2.waitKey(1) == ord('q'):
            break
