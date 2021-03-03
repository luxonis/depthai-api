#!/usr/bin/env python3

import cv2
import depthai as dai


def print_sys_info(info):
    m = 1024 * 1024 # MiB
    print(f"Drr used / total - {info.ddrMemoryUsage.used / m:.2f} / {info.ddrMemoryUsage.total / m:.2f} MiB")
    # Add binding first
    # print(f"Cmx used / total - {info.cmxMemoryUsage.used / m:.2f} / {info.cmxMemoryUsage.total / m:.2f} MiB")
    print(f"LeonCss heap used / total - {info.leonCssMemoryUsage.used / m:.2f} / {info.leonCssMemoryUsage.total / m:.2f} MiB")
    print(f"LeonMss heap used / total - {info.leonMssMemoryUsage.used / m:.2f} / {info.leonMssMemoryUsage.total / m:.2f} MiB")
    t = info.chipTemperature;
    print(f"Chip temperature - average: {t.average:.2f}, css: {t.css:.2f}, mss: {t.mss:.2f}, upa0: {t.upa:.2f}, upa1: {t.dss:.2f}")
    print(f"Cpu usage - Leon OS: {info.leonCssCpuUsage.average * 100:.2f}%, Leon RT: {info.leonMssCpuUsage.average * 100:.2f} %")
    print("----------------------------------------")

# Start defining a pipeline
pipeline = dai.Pipeline()

sys_logger = pipeline.createSystemLogger()
sys_logger.setRate(1) # 1 Hz

# Create output
link_out = pipeline.createXLinkOut()
link_out.setStreamName("sysinfo")
sys_logger.out.link(link_out.input)

# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    # Output queue will be used to get the system info
    q_sysinfo = device.getOutputQueue(name="sysinfo", maxSize=4, blocking=False)

    while True:
        info = q_sysinfo.get()  # blocking call, will wait until a new data has arrived
        print_sys_info(info)

        if cv2.waitKey(1) == ord('q'):
            break

