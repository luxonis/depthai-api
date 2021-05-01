#!/usr/bin/env python3

import cv2
import numpy as np
import depthai as dai
from time import sleep
import datetime
import argparse
from pathlib import Path

datasetDefault = str((Path(__file__).parent / Path('dataset')).resolve().absolute())
parser = argparse.ArgumentParser()
parser.add_argument('-dataset', nargs='?', help="Path to recorded frames", default=datasetDefault)
args = parser.parse_args()

if not Path(datasetDefault).exists():
    import sys
    raise FileNotFoundError(f'Required file/s not found, please run "{sys.executable} install_requirements.py"')


# StereoDepth config options.
out_depth = False  # Disparity by default
out_rectified = True   # Output and display rectified streams
lrcheck = True   # Better handling for occlusions
extended = False  # Closer-in minimum depth, disparity range is doubled
subpixel = True   # Better accuracy for longer distance, fractional disparity 32-levels
median = dai.StereoDepthProperties.MedianFilter.KERNEL_7x7

# Sanitize some incompatible options
if lrcheck or extended or subpixel:
    median = dai.StereoDepthProperties.MedianFilter.MEDIAN_OFF

print("StereoDepth config options: ")
print("Left-Right check: ", lrcheck)
print("Extended disparity: ", extended)
print("Subpixel: ", subpixel)
print("Median filtering: ", median)

right_intrinsic = [[860.0, 0.0, 640.0], [0.0, 860.0, 360.0], [0.0, 0.0, 1.0]]


def create_stereo_depth_pipeline():
    print("Creating Stereo Depth pipeline: ", end='')

    print("XLINK IN -> STEREO -> XLINK OUT")
    pipeline = dai.Pipeline()

    camLeft = pipeline.createXLinkIn()
    camRight = pipeline.createXLinkIn()
    stereo = pipeline.createStereoDepth()
    xoutLeft = pipeline.createXLinkOut()
    xoutRight = pipeline.createXLinkOut()
    xoutDepth = pipeline.createXLinkOut()
    xoutDisparity = pipeline.createXLinkOut()
    xoutRectifLeft = pipeline.createXLinkOut()
    xoutRectifRight = pipeline.createXLinkOut()

    camLeft.setStreamName('in_left')
    camRight.setStreamName('in_right')

    stereo.setOutputDepth(out_depth)
    stereo.setOutputRectified(out_rectified)
    stereo.setConfidenceThreshold(200)
    stereo.setRectifyEdgeFillColor(0) # Black, to better see the cutout
    stereo.setMedianFilter(median) # KERNEL_7x7 default
    stereo.setLeftRightCheck(lrcheck)
    stereo.setExtendedDisparity(extended)
    stereo.setSubpixel(subpixel)

    stereo.setEmptyCalibration() # Set if the input frames are already rectified
    stereo.setInputResolution(1280, 720)

    xoutLeft.setStreamName('left')
    xoutRight.setStreamName('right')
    xoutDepth.setStreamName('depth')
    xoutDisparity.setStreamName('disparity')
    xoutRectifLeft.setStreamName('rectified_left')
    xoutRectifRight.setStreamName('rectified_right')

    camLeft.out.link(stereo.left)
    camRight.out.link(stereo.right)
    stereo.syncedLeft.link(xoutLeft.input)
    stereo.syncedRight.link(xoutRight.input)
    stereo.depth.link(xoutDepth.input)
    stereo.disparity.link(xoutDisparity.input)
    stereo.rectifiedLeft.link(xoutRectifLeft.input)
    stereo.rectifiedRight.link(xoutRectifRight.input)

    streams = ['left', 'right']
    if out_rectified:
        streams.extend(['rectified_left', 'rectified_right'])
    streams.extend(['disparity', 'depth'])

    return pipeline, streams


def convert_to_cv2_frame(name, image):
    baseline = 75 #mm
    focal = right_intrinsic[0][0]
    max_disp = 96
    disp_type = np.uint8
    disp_levels = 1
    if (extended):
        max_disp *= 2
    if (subpixel):
        max_disp *= 32
        disp_type = np.uint16
        disp_levels = 32

    data, w, h = image.getData(), image.getWidth(), image.getHeight()
    if name == 'depth':
        # this contains FP16 with (lrcheck or extended or subpixel)
        frame = np.array(data).astype(np.uint8).view(np.uint16).reshape((h, w))
    elif name == 'disparity':
        disp = np.array(data).astype(np.uint8).view(disp_type).reshape((h, w))

        # Compute depth from disparity
        with np.errstate(divide='ignore'):
            depth = (disp_levels * baseline * focal / disp).astype(np.uint16)

        if 1: # Optionally, extend disparity range to better visualize it
            frame = (disp * 255. / max_disp).astype(np.uint8)

        if 1: # Optionally, apply a color map
            frame = cv2.applyColorMap(frame, cv2.COLORMAP_HOT)

    else: # mono streams / single channel
        frame = np.array(data).reshape((h, w)).astype(np.uint8)
        if name.startswith('rectified_'):
            frame = cv2.flip(frame, 1)
        if name == 'rectified_right':
            last_rectif_right = frame
    return frame


pipeline, streams = create_stereo_depth_pipeline()

print("Creating DepthAI device")
with dai.Device(pipeline) as device:
    print("Starting pipeline")
    device.startPipeline()

    inStreams = ['in_right', 'in_left']
    inStreamsCameraID = [dai.CameraBoardSocket.RIGHT, dai.CameraBoardSocket.LEFT]
    in_q_list = []
    for s in inStreams:
        q = device.getInputQueue(s)
        in_q_list.append(q)

    # Create a receive queue for each stream
    q_list = []
    for s in streams:
        q = device.getOutputQueue(s, 8, blocking=False)
        q_list.append(q)

    # Need to set a timestamp for input frames, for the sync stage in Stereo node
    timestamp_ms = 0
    index = 0
    while True:
        # Handle input streams, if any
        if in_q_list:
            dataset_size = 2  # Number of image pairs
            frame_interval_ms = 500
            for i, q in enumerate(in_q_list):
                path = args.dataset + '/' + str(index) + '/' + q.getName() + '.png'
                data = cv2.imread(path, cv2.IMREAD_GRAYSCALE).reshape(720*1280)
                tstamp = datetime.timedelta(seconds = timestamp_ms // 1000,
                                            milliseconds = timestamp_ms % 1000)
                img = dai.ImgFrame()
                img.setData(data)
                img.setTimestamp(tstamp)
                img.setInstanceNum(inStreamsCameraID[i])
                img.setType(dai.ImgFrame.Type.RAW8)
                img.setWidth(1280)
                img.setHeight(720)
                q.send(img)
                if timestamp_ms == 0:  # Send twice for first iteration
                    q.send(img)
                print("Sent frame: {:25s}".format(path), 'timestamp_ms:', timestamp_ms)
            timestamp_ms += frame_interval_ms
            index = (index + 1) % dataset_size
            sleep(frame_interval_ms / 1000)
        # Handle output streams
        for q in q_list:
            if q.getName() in ['left', 'right', 'depth']: continue
            frame = convert_to_cv2_frame(q.getName(), q.get())
            cv2.imshow(q.getName(), frame)
        if cv2.waitKey(1) == ord('q'):
            break
