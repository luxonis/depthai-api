24 - RGB & TinyYoloV4 decoding on device
==========================================

This example shows how to run TinyYoloV4 on the RGB input frame, and how to display both the RGB
preview and the metadata results from the TinyYoloV4 on the preview. Decoding is done on Myriad instead on the host.

Configurable, network dependent parameters are required for correct decoding:
setNumClasses - number of YOLO classes
setCoordinateSize - size of coordinate
setAnchors - yolo anchors
setAnchorMasks - anchorMasks26, anchorMasks13 (anchorMasks52 - additionally for full YOLOv4)
setIouThreshold - intersection over union threshold
setConfidenceThreshold - confidence threshold above which objects are detected

Demo
####


Setup
#####

Please run the following command to install the required dependencies

.. code-block:: bash

  python3 -m pip install --extra-index-url https://artifacts.luxonis.com/artifactory/luxonis-python-snapshot-local/ depthai==0.0.2.1+d351f436f596a0e2ae9881f539b3e5a7fe714bfe numpy==1.19.5 opencv-python==4.5.1.48

For additional information, please follow :ref:`Python API installation guide <Installation - Python>`

This example also requires YOLOv4-tiny blob (:code:`tiny-yolo-v4_openvino_2021.2_6shave.blob` file) to work - you can download it from
`here <https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/tiny-yolo-v4_openvino_2021.2_6shave.blob>`__

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/gen2_develop/examples/24_tiny_yolo_v4_device_side_decoding.py>`__

.. literalinclude:: ../../../examples/24_tiny_yolo_v4_device_side_decoding.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
