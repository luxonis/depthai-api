26.2 - Mono & MobilenetSSD with spatial data
============================================

This example shows how to run MobileNetv2SSD on the rectified right input frame, and
how to display both the  preview, detections, depth map and spatial information (X,Y,Z).
It's similar to example '21_mobilenet_decoding_on_device' except it has spatial data.
X,Y,Z coordinates are relative to the center of depth map.

setConfidenceThreshold - confidence threshold above which objects are detected

Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/SZz7NwM86uw" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>


Setup
#####

.. include::  /includes/install_from_pypi.rst


This example also requires MobilenetSDD blob (:code:`mobilenet-ssd_openvino_2021.2_6shave.blob` file) to work - you can download it from
`here <https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/mobilenet-ssd_openvino_2021.2_6shave.blob>`__

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/main/examples/26_2_spatial_mobilenet_mono.py>`__

.. literalinclude:: ../../../examples/26_2_spatial_mobilenet_mono.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
