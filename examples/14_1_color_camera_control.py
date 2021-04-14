#!/usr/bin/env python3

"""
This example shows usage of Camera Control message as well as ColorCamera configInput to change crop x and y
Uses 'WASD' controls to move the crop window, 'C' to capture a still image, 'T' to trigger autofocus, 'IOKL,.'
for manual exposure/focus:
  Control:      key[dec/inc]  min..max
  exposure time:     I   O      1..33000 [us]
  sensitivity iso:   K   L    100..1600
  focus:             ,   .      0..255 [far..near]
To go back to auto controls:
  'E' - autoexposure
  'F' - autofocus (continuous)
"""

import depthai as dai
import cv2

# Step size ('W','A','S','D' controls)
STEP_SIZE = 8
# Manual exposure/focus set step
EXP_STEP = 500  # us
ISO_STEP = 50
LENS_STEP = 3

pipeline = dai.Pipeline()

# Nodes
colorCam = pipeline.createColorCamera()
controlIn = pipeline.createXLinkIn()
configIn = pipeline.createXLinkIn()
videoEncoder = pipeline.createVideoEncoder()
stillEncoder = pipeline.createVideoEncoder()
videoMjpegOut = pipeline.createXLinkOut()
stillMjpegOut = pipeline.createXLinkOut()
previewOut = pipeline.createXLinkOut()


# Properties
colorCam.setVideoSize(640, 360)
colorCam.setPreviewSize(300, 300)
controlIn.setStreamName('control')
configIn.setStreamName('config')
videoEncoder.setDefaultProfilePreset(colorCam.getVideoSize(), colorCam.getFps(), dai.VideoEncoderProperties.Profile.MJPEG)
stillEncoder.setDefaultProfilePreset(colorCam.getStillSize(), 1, dai.VideoEncoderProperties.Profile.MJPEG)
videoMjpegOut.setStreamName('video')
stillMjpegOut.setStreamName('still')
previewOut.setStreamName('preview')


# Link nodes
colorCam.video.link(videoEncoder.input)
colorCam.still.link(stillEncoder.input)
colorCam.preview.link(previewOut.input)
controlIn.out.link(colorCam.inputControl)
configIn.out.link(colorCam.inputConfig)
videoEncoder.bitstream.link(videoMjpegOut.input)
stillEncoder.bitstream.link(stillMjpegOut.input)


def clamp(num, v0, v1):
    return max(v0, min(num, v1))


# Pipeline is defined, now we can connect to the device
with dai.Device(pipeline) as dev:

    # Get data queues
    controlQueue = dev.getInputQueue('control')
    configQueue = dev.getInputQueue('config')
    previewQueue = dev.getOutputQueue('preview')
    videoQueue = dev.getOutputQueue('video')
    stillQueue = dev.getOutputQueue('still')

    # Start pipeline
    dev.startPipeline()

    # Max cropX & cropY
    maxCropX = (colorCam.getResolutionWidth() - colorCam.getVideoWidth()) / colorCam.getResolutionWidth()
    maxCropY = (colorCam.getResolutionHeight() - colorCam.getVideoHeight()) / colorCam.getResolutionHeight()

    # Default crop
    cropX = 0
    cropY = 0
    sendCamConfig = True

    # Defaults and limits for manual focus/exposure controls
    lensPos = 150
    lensMin = 0
    lensMax = 255

    expTime = 20000
    expMin = 1
    expMax = 33000

    sensIso = 800
    sensMin = 100
    sensMax = 1600

    while True:

        previewFrames = previewQueue.tryGetAll()
        for previewFrame in previewFrames:
            cv2.imshow('preview', previewFrame.getData().reshape(previewFrame.getWidth(), previewFrame.getHeight(), 3))

        videoFrames = videoQueue.tryGetAll()
        for videoFrame in videoFrames:
            # Decode JPEG
            frame = cv2.imdecode(videoFrame.getData(), cv2.IMREAD_UNCHANGED)
            # Display
            cv2.imshow('video', frame)

            # Send new cfg to camera
            if sendCamConfig:
                cfg = dai.ImageManipConfig()
                cfg.setCropRect(cropX, cropY, 0, 0)
                configQueue.send(cfg)
                print('Sending new crop - x: ', cropX, ' y: ', cropY)
                sendCamConfig = False

        stillFrames = stillQueue.tryGetAll()
        for stillFrame in stillFrames:
            # Decode JPEG
            frame = cv2.imdecode(stillFrame.getData(), cv2.IMREAD_UNCHANGED)
            # Display
            cv2.imshow('still', frame)


        # Update screen
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('c'):
            ctrl = dai.CameraControl()
            ctrl.setCaptureStill(True)
            controlQueue.send(ctrl)
        elif key == ord('t'):
            print("Autofocus trigger (and disable continuous)")
            ctrl = dai.CameraControl()
            ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)
            ctrl.setAutoFocusTrigger()
            controlQueue.send(ctrl)
        elif key == ord('f'):
            print("Autofocus enable, continuous")
            ctrl = dai.CameraControl()
            ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.CONTINUOUS_VIDEO)
            controlQueue.send(ctrl)
        elif key == ord('e'):
            print("Autoexposure enable")
            ctrl = dai.CameraControl()
            ctrl.setAutoExposureEnable()
            controlQueue.send(ctrl)
        elif key in [ord(','), ord('.')]:
            if key == ord(','): lensPos -= LENS_STEP
            if key == ord('.'): lensPos += LENS_STEP
            lensPos = clamp(lensPos, lensMin, lensMax)
            print("Setting manual focus, lens position:", lensPos)
            ctrl = dai.CameraControl()
            ctrl.setManualFocus(lensPos)
            controlQueue.send(ctrl)
        elif key in [ord('i'), ord('o'), ord('k'), ord('l')]:
            if key == ord('i'): expTime -= EXP_STEP
            if key == ord('o'): expTime += EXP_STEP
            if key == ord('k'): sensIso -= ISO_STEP
            if key == ord('l'): sensIso += ISO_STEP
            expTime = clamp(expTime, expMin, expMax)
            sensIso = clamp(sensIso, sensMin, sensMax)
            print("Setting manual exposure, time:", expTime, "iso:", sensIso)
            ctrl = dai.CameraControl()
            ctrl.setManualExposure(expTime, sensIso)
            controlQueue.send(ctrl)
        elif key in [ord('w'), ord('a'), ord('s'), ord('d')]:
            if key == ord('a'):
                cropX = cropX - (maxCropX / colorCam.getResolutionWidth()) * STEP_SIZE
                if cropX < 0: cropX = maxCropX
            elif key == ord('d'):
                cropX = cropX + (maxCropX / colorCam.getResolutionWidth()) * STEP_SIZE
                if cropX > maxCropX: cropX = 0
            elif key == ord('w'):
                cropY = cropY - (maxCropY / colorCam.getResolutionHeight()) * STEP_SIZE
                if cropY < 0: cropY = maxCropY
            elif key == ord('s'):
                cropY = cropY + (maxCropY / colorCam.getResolutionHeight()) * STEP_SIZE
                if cropY > maxCropY: cropY = 0
            sendCamConfig = True
