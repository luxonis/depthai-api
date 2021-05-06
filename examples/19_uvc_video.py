#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-fb', '--flash-bootloader', default=False, action="store_true")
parser.add_argument('-f',  '--flash-app',        default=False, action="store_true")
parser.add_argument('-l',  '--logs',             default=False, action="store_true")
args = parser.parse_args()

if args.logs:
    import os
    os.environ["DEPTHAI_LEVEL"] = "info"

import time
import depthai as dai

enable_4k = True

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - color camera
cam_rgb = pipeline.createColorCamera()
cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
cam_rgb.setInterleaved(False)
cam_rgb.setPreviewSize(1920, 1080)
cam_rgb.initialControl.setManualFocus(130)
# Note: this file contains tuning info for all cameras, but for now setting it
#       at pipeline level is not supported, so we set it for ColorCamera
#cam_rgb.setCameraTuningBlobPath('/home/user/customTuning.bin')

if enable_4k:
    cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
    cam_rgb.setIspScale(1, 2)
else:
    cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)

# Create an UVC (USB Video Class) output node
uvc = pipeline.createUVC()
cam_rgb.video.link(uvc.input)

if args.flash_bootloader or args.flash_app:
    (f, bl) = dai.DeviceBootloader.getFirstAvailableDevice()
    bootloader = dai.DeviceBootloader(bl)
    progress = lambda p : print(f'Flashing progress: {p*100:.1f}%')
    if args.flash_bootloader:
        print("Flashing bootloader...")
        bootloader.flashBootloader(progress)
        print("Note: make sure to change DIP switch to 0x8 (001000), if not done already")
    else:
        print("Flashing application pipeline...")
        bootloader.flash(progress, pipeline)
    print("Done. Exiting.")
    quit()

# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    print("\nDevice started, please keep this process running")
    print("and open an UVC viewer. Example on Linux:")
    print("    guvcview -d /dev/video0")
    print("\nTo close: Ctrl+C")

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break
