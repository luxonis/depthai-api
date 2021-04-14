22.1 - RGB & TinyYoloV3 decoding on device
==========================================

This example shows how to run TinyYoloV3 on the RGB input frame, and how to display both the RGB
preview and the metadata results from the TinyYoloV3 on the preview. Decoding is done on Myriad instead on the host.

Configurable, network dependent parameters are required for correct decoding:
setNumClasses - number of YOLO classes
setCoordinateSize - size of coordinate
setAnchors - yolo anchors
setAnchorMasks - anchorMasks26, anchorMasks13 (anchorMasks52 - additionally for full YOLOv3)
setIouThreshold - intersection over union threshold
setConfidenceThreshold - confidence threshold above which objects are detected

Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/2zXyYzD7ESQ" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>


Setup
#####

.. include::  /includes/install_from_pypi.rst

This example also requires YoloV3-tiny blob (:code:`tiny-yolo-v3_openvino_2021.2_6shave.blob` file) to work - you can download it from
`here <https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/tiny-yolo-v3_openvino_2021.2_6shave.blob>`__

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/main/examples/22_1_tiny_yolo_v3_device_side_decoding.py>`__

.. literalinclude:: ../../../examples/22_1_tiny_yolo_v3_device_side_decoding.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
