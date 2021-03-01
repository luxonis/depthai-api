#!/usr/bin/env python3

import time
from pathlib import Path

import cv2
import depthai as dai

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - color camera
cam_rgb = pipeline.createColorCamera()
cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)

# Create RGB output
xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("rgb")
cam_rgb.video.link(xout_rgb.input)

# Create encoder to produce JPEG images
video_enc = pipeline.createVideoEncoder()
video_enc.setDefaultProfilePreset(cam_rgb.getVideoSize(), cam_rgb.getFps(), dai.VideoEncoderProperties.Profile.MJPEG)
cam_rgb.video.link(video_enc.input)

# Create JPEG output
xout_jpeg = pipeline.createXLinkOut()
xout_jpeg.setStreamName("jpeg")
video_enc.bitstream.link(xout_jpeg.input)


# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    # Output queue will be used to get the rgb frames from the output defined above
    q_rgb = device.getOutputQueue(name="rgb", maxSize=30, blocking=False)
    q_jpeg = device.getOutputQueue(name="jpeg", maxSize=30, blocking=True)

    # Make sure the destination path is present before starting to store the examples
    Path('06_data').mkdir(parents=True, exist_ok=True)

    while True:
        in_rgb = q_rgb.tryGet()  # non-blocking call, will return a new data that has arrived or None otherwise

        if in_rgb is not None:
            # data is originally represented as a flat 1D array, it needs to be converted into HxW form
            shape = (in_rgb.getHeight() * 3 // 2, in_rgb.getWidth())
            frame_rgb = cv2.cvtColor(in_rgb.getData().reshape(shape), cv2.COLOR_YUV2BGR_NV12)
            # frame is transformed and ready to be shown
            cv2.imshow("rgb", frame_rgb)

        for enc_frame in q_jpeg.tryGetAll():
            with open(f"06_data/{int(time.time() * 10000)}.jpeg", "wb") as f:
                f.write(bytearray(enc_frame.getData()))

        if cv2.waitKey(1) == ord('q'):
            break
