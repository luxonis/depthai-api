#!/usr/bin/env python3

''' This example shows usage of Camera Control message as well as ColorCamera configInput to change crop x and y
Uses 'WASD' controls to move the crop window, 'C' to capture a still image, 'T' to trigger autofocus, 'IOKL,.'
for manual exposure/focus:
  Control:      key[dec/inc]  min..max
  exposure time:     I   O      1..33000 [us]
  sensitivity iso:   K   L    100..1600
  focus:             ,   .      0..255 [far..near]
To go back to auto controls:
  'E' - autoexposure
  'F' - autofocus (continuous)
'''

import depthai as dai
import cv2
import numpy as np

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

def clamp(num, v0, v1): return max(v0, min(num, v1))

# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as dev:

    # Get data queues
    controlQueue = dev.getInputQueue('control')
    configQueue = dev.getInputQueue('config')
    previewQueue = dev.getOutputQueue('preview')
    videoQueue = dev.getOutputQueue('video')
    stillQueue = dev.getOutputQueue('still')

    # Start pipeline
    dev.startPipeline()

    # Max crop_x & crop_y
    max_crop_x = (colorCam.getResolutionWidth() - colorCam.getVideoWidth()) / colorCam.getResolutionWidth()
    max_crop_y = (colorCam.getResolutionHeight() - colorCam.getVideoHeight()) / colorCam.getResolutionHeight()

    # Default crop
    crop_x = 0
    crop_y = 0
    send_cam_config = True

    # Defaults and limits for manual focus/exposure controls
    lens_pos = 150
    lens_min = 0
    lens_max = 255

    exp_time = 20000
    exp_min = 1
    exp_max = 33000

    sens_iso = 800
    sens_min = 100
    sens_max = 1600

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
            if send_cam_config:
                cfg = dai.ImageManipConfig()
                cfg.setCropRect(crop_x, crop_y, 0, 0)
                configQueue.send(cfg)
                print('Sending new crop - x: ', crop_x, ' y: ', crop_y)
                send_cam_config = False

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
            if key == ord(','): lens_pos -= LENS_STEP
            if key == ord('.'): lens_pos += LENS_STEP
            lens_pos = clamp(lens_pos, lens_min, lens_max)
            print("Setting manual focus, lens position:", lens_pos)
            ctrl = dai.CameraControl()
            ctrl.setManualFocus(lens_pos)
            controlQueue.send(ctrl)
        elif key in [ord('i'), ord('o'), ord('k'), ord('l')]:
            if key == ord('i'): exp_time -= EXP_STEP
            if key == ord('o'): exp_time += EXP_STEP
            if key == ord('k'): sens_iso -= ISO_STEP
            if key == ord('l'): sens_iso += ISO_STEP
            exp_time = clamp(exp_time, exp_min, exp_max)
            sens_iso = clamp(sens_iso, sens_min, sens_max)
            print("Setting manual exposure, time:", exp_time, "iso:", sens_iso)
            ctrl = dai.CameraControl()
            ctrl.setManualExposure(exp_time, sens_iso)
            controlQueue.send(ctrl)
        elif key in [ord('w'), ord('a'), ord('s'), ord('d')]:
            if key == ord('a'):
                crop_x = crop_x - (max_crop_x / colorCam.getResolutionWidth()) * STEP_SIZE
                if crop_x < 0: crop_x = max_crop_x
            elif key == ord('d'):
                crop_x = crop_x + (max_crop_x / colorCam.getResolutionWidth()) * STEP_SIZE
                if crop_x > max_crop_x: crop_x = 0
            elif key == ord('w'):
                crop_y = crop_y - (max_crop_y / colorCam.getResolutionHeight()) * STEP_SIZE
                if crop_y < 0: crop_y = max_crop_y
            elif key == ord('s'):
                crop_y = crop_y + (max_crop_y / colorCam.getResolutionHeight()) * STEP_SIZE
                if crop_y > max_crop_y: crop_y = 0
            send_cam_config = True
