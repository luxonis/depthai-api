#!/usr/bin/env python3

'''
This example shows usage of ImageWarp to crop a rotated rectangle area on a frame,
or perform various image transforms: rotate, mirror, flip, perspective transform.
'''

import depthai as dai
import cv2
import numpy as np

key_rotate_decr = 'z'
key_rotate_incr = 'x'
key_resize_inc = 'v'
key_warp_test_cycle = 'c'

def print_controls():
    print("=== Controls:")
    print(key_rotate_decr, "-rotated rectangle crop, decrease rate")
    print(key_rotate_incr, "-rotated rectangle crop, increase rate")
    print(key_warp_test_cycle, "-warp 4-point transform, cycle through modes")
    print(key_resize_inc, "-resize cropped region, or disable resize")
    print("h -print controls (help)")

rotate_rate_max = 5.0
rotate_rate_inc = 0.1

resize_max_w = 800
resize_max_h = 600
resize_factor_max = 5

'''
The crop points are specified in clockwise order,
with first point mapped to output top-left, as:
    P0  ->  P1
     ^       v
    P3  <-  P2
'''
P0 = [0, 0]  # top-left
P1 = [1, 0]  # top-right
P2 = [1, 1]  # bottom-right
P3 = [0, 1]  # bottom-left
warp_test_list = [
    # points order, normalized cordinates, description
    #[[[0,0],[1,0],[1,1],[0,1]], True, "passthrough"],
    #[[[0,0],[639,0],[639,479],[0,479]], False, "passthrough (pixels)"],
    [[P0, P1, P2, P3], True, "1.passthrough"],
    [[P3, P0, P1, P2], True, "2.rotate 90"],
    [[P2, P3, P0, P1], True, "3.rotate 180"],
    [[P1, P2, P3, P0], True, "4.rotate 270"],
    [[P1, P0, P3, P2], True, "5.horizontal mirror"],
    [[P3, P2, P1, P0], True, "6.vertical flip"],
    [[[-0.1,-0.1],[1.1,-0.1],[1.1,1.1],[-0.1,1.1]], True, "7.add black borders"],
    [[[-0.3, 0],[1, 0],[1.3, 1],[0, 1]], True, "8.parallelogram transform"],
    [[[-0.2, 0],[1.8, 0],[1, 1],[0, 1]], True, "9.trapezoid transform"],
]

pipeline = dai.Pipeline()

cam = pipeline.createColorCamera()
cam.setPreviewSize(640, 480)
cam.setInterleaved(False)
cam_out = pipeline.createXLinkOut()
cam_out.setStreamName("preview")

manip = pipeline.createImageManip()
manip.setMaxOutputFrameSize(2000*1500*3)
manip_out = pipeline.createXLinkOut()
manip_out.setStreamName("manip")
manip_cfg = pipeline.createXLinkIn()
manip_cfg.setStreamName("manip_cfg")

cam.preview.link(cam_out.input)
cam.preview.link(manip.inputImage)
manip.out.link(manip_out.input)
manip_cfg.out.link(manip.inputConfig)

with dai.Device(pipeline) as device:
    device.startPipeline()

    q_preview = device.getOutputQueue(name="preview", maxSize=4)
    q_manip = device.getOutputQueue(name="manip", maxSize=4)
    q_manip_cfg = device.getInputQueue(name="manip_cfg")

    key = -1
    angle_deg = 0
    rotate_rate = 1.0
    resize_factor = 0
    resize_x = 0
    resize_y = 0
    test_four_pt = False
    warp_idx = -1

    print_controls()

    while key != ord('q'):
        if key > 0:
            if key == ord(key_rotate_decr) or key == ord(key_rotate_incr):
                if key == ord(key_rotate_decr):
                    if rotate_rate > -rotate_rate_max: rotate_rate -= rotate_rate_inc
                if key == ord(key_rotate_incr):
                    if rotate_rate <  rotate_rate_max: rotate_rate += rotate_rate_inc
                test_four_pt = False
                print("Crop rotated rectangle, rate per frame: {:.1f} degrees."
                      .format(rotate_rate))
            elif key == ord(key_resize_inc):
                resize_factor += 1
                if resize_factor > resize_factor_max:
                    resize_factor = 0
                    print("Crop region not resized")
                else:
                    resize_x = resize_max_w // resize_factor
                    resize_y = resize_max_h // resize_factor
                    print("Crop region resized to", resize_x, 'x', resize_y)
            elif key == ord(key_warp_test_cycle):
                # Disable resizing initially
                resize_factor = 0
                warp_idx = (warp_idx + 1) % len(warp_test_list)
                test_four_pt = True
                test_description = warp_test_list[warp_idx][2]
                print("Warp 4-point transform:", test_description)
            elif key == ord('h'):
                print_controls()

        # Send an updated config with continuous rotate, or after a key press
        if key >= 0 or (not test_four_pt and abs(rotate_rate) > 0.0001):
            cfg = dai.ImageManipConfig()
            if test_four_pt:
                test = warp_test_list[warp_idx]
                points, normalized = test[0], test[1]
                # TODO: improve this, should avoid this conversion
                point2f_list = []
                for p in points:
                    pt = dai.Point2f()
                    pt.x, pt.y = p[0], p[1]
                    point2f_list.append(pt)
                cfg.setWarpTransformFourPoints(point2f_list, normalized)
            else:
                angle_deg += rotate_rate
                rotated_rect = ((320, 240), (400, 400), angle_deg)
                rr = dai.RotatedRect()
                rr.center.x,   rr.center.y    = rotated_rect[0]
                rr.size.width, rr.size.height = rotated_rect[1]
                rr.angle                      = rotated_rect[2]
                cfg.setCropRotatedRect(rr, False)
            if resize_factor > 0:
                cfg.setResize(resize_x, resize_y)
            #cfg.setWarpBorderFillColor(0, 0, 255)
            #cfg.setWarpBorderReplicatePixels()
            q_manip_cfg.send(cfg)

        for q in [q_preview, q_manip]:
            pkt = q.get()
            name = q.getName()
            shape = (3, pkt.getHeight(), pkt.getWidth())
            frame = pkt.getData().reshape(shape).transpose(1, 2, 0)
            frame = np.ascontiguousarray(frame)
            if name == "preview" and not test_four_pt:
                # Draw RotatedRect cropped area on input frame
                points = np.int0(cv2.boxPoints(rotated_rect))
                cv2.drawContours(frame, [points], 0, (255,0,0), 1)
                # Mark top-left corner
                cv2.circle(frame, tuple(points[1]), 10, (255,0,0), 2)
            cv2.imshow(name, frame)
        key = cv2.waitKey(1)
