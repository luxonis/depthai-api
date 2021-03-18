#!/usr/bin/env python3

# This example demonstrates use of queue events to block a thread until a message
# arrives to any (of the specified) queue

import cv2
import depthai as dai

# Start defining a pipeline
pipeline = dai.Pipeline()

# Create Color and Mono cameras
cam_rgb = pipeline.createColorCamera()
cam_mono = pipeline.createMonoCamera()
# Create separate streams for them
xout_rgb = pipeline.createXLinkOut()
xout_mono = pipeline.createXLinkOut()

# Set properties
xout_rgb.setStreamName("rgb")
xout_mono.setStreamName("mono")
# Cap color camera to 5 fps
cam_rgb.setFps(5)
cam_rgb.setInterleaved(True)
cam_rgb.setPreviewSize(300, 300)

# Connect
cam_rgb.preview.link(xout_rgb.input)
cam_mono.out.link(xout_mono.input)


# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()
        
    # Clear queue events
    device.getQueueEvents()

    while True:
        # Block until a message arrives to any of the specified queues
        queueName = device.getQueueEvent(("rgb", "mono"))

        # Getting that message from queue with name specified by the event
        # Note: number of events doesn't necessarily match number of messages in queues
        # because queues can be set to non-blocking (overwriting) behavior
        message = device.getOutputQueue(queueName).get()

        # display arrived frames
        if type(message) == dai.ImgFrame:
            cv2.imshow(queueName, message.getCvFrame())

        if cv2.waitKey(1) == ord('q'):
            break
