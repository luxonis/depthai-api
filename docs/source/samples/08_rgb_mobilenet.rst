08 - RGB & MobilenetSSD
=======================

This example shows how to run MobileNetv2SSD on the RGB input frame, and how to display both the RGB
preview and the metadata results from the MobileNetv2SSD on the preview.

Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/68VkKGO1WX4" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>

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

.. tabs::

    .. tab:: C++

        Also `available on GitHub <https://github.com/luxonis/depthai-core/blob/develop/examples/src/08_rgb_mobilenet.cpp>`__

        .. literalinclude:: ../../../depthai-core/examples/src/08_rgb_mobilenet.cpp
           :language: python
           :linenos:

    .. tab:: Python

        Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/develop/examples/08_rgb_mobilenet.py>`__

        .. literalinclude:: ../../../examples/08_rgb_mobilenet.py
           :language: python
           :linenos:

.. include::  /includes/footer-short.rst
