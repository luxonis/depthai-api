from depthai import CameraControl

def stillCapture():
    ctrl = CameraControl()
    ctrl.setCaptureStill(True)
    while True:
        node.io['out'].send(ctrl)

def stillCaptureEverySecond():
    import time
    ctrl = CameraControl()
    ctrl.setCaptureStill(True)
    while True:
        time.sleep(1)
        node.io['out'].send(ctrl)
