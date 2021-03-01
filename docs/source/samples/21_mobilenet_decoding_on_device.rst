21 - RGB & MobilenetSSD decoding on device
==========================================

This example shows how to run MobileNetv2SSD on the RGB input frame, and how to display both the RGB
preview and the metadata results from the MobileNetv2SSD on the preview. It's similar to example '08_rgb_mobilenet' except
decoding is done on Myriad instead on the host.


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
`here <https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/mobilenet-ssd_openvino_2021.2_6shave.blob>`__

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/gen2_develop/examples/21_mobilenet_device_side_decoding.py>`__

.. tabs::

    .. tab:: C++

        Also `available on GitHub <https://github.com/luxonis/depthai-core/blob/gen2_develop/examples/src/21_mobilenet_device_side_decoding.cpp>`__

        .. literalinclude:: ../../../depthai-core/examples/src/21_mobilenet_device_side_decoding.cpp
           :language: python
           :linenos:

    .. tab:: Python

        Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/gen2_develop/examples/21_mobilenet_device_side_decoding.py>`__

        .. literalinclude:: ../../../examples/21_mobilenet_device_side_decoding.py
           :language: python
           :linenos:

.. include::  /includes/footer-short.rst
