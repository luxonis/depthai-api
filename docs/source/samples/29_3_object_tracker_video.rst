29.3 - Object tracker on video
==============================

This example shows how to run MobileNetv2SSD on video input frame, and perform object tracking on persons.

Demo
####


Setup
#####

.. include::  /includes/install_from_pypi.rst


This example also requires MobilenetSDD based person-detection blob (:code:`person-detection-0201_openvino_2021.3_7shave.blob` file) to work - you can download it from
`here <https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/person-detection-0201_openvino_2021.3_7shave.blob>`__

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/gen2_develop/examples/29_3_object_tracker_video.py>`__

.. literalinclude:: ../../../examples/29_3_object_tracker_video.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
