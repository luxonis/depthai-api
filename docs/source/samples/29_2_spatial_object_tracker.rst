29.2 - Spatial object tracker on RGB camera
===========================================

This example shows how to run MobileNetv2SSD on the RGB input frame, and perform spatial object tracking on persons.

Demo
####


Setup
#####

.. include::  /includes/install_from_pypi.rst


This example also requires MobilenetSDD blob (:code:`mobilenet.blob` file) to work - you can download it from
`here <https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/mobilenet-ssd_openvino_2021.2_6shave.blob>`__

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/gen2_develop/examples/29_2_spatial_object_tracker.py>`__

.. literalinclude:: ../../../examples/29_2_spatial_object_tracker.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
