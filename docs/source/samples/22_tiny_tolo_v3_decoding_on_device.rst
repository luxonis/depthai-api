21 - RGB & TinyYoloV3 decoding on device
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


Setup
#####

Please run the following command to install the required dependencies

.. code-block:: bash
  :substitutions:

  python3 -m pip install --extra-index-url https://artifacts.luxonis.com/artifactory/luxonis-python-snapshot-local/ depthai==|release| numpy==1.19.5 opencv-python==4.5.1.48


For additional information, please follow :ref:`Python API installation guide <Installation - Python>`

This example also requires MobilenetSDD blob (:code:`mobilenet.blob` file) to work - you can download it from
`here <https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/tiny-yolo-v3_openvino_2021.2_6shave.blob>`__

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/gen2_develop/examples/22_tiny_yolo_v3_device_side_decoding.py>`__

.. literalinclude:: ../../../examples/22_tiny_yolo_v3_device_side_decoding.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
