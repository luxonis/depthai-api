15 - 4K RGB MobileNetSSD
========================

This example shows how to MobileNetv2SSD on the RGB input frame, and how to display both the RGB
preview and the metadata results from the MobileNetv2SSD on the preview.
The preview size is set to 4K resolution

Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/Ww-vLSxOdW8" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>


Setup
#####

Please run the following command to install the required dependencies

.. code-block:: bash
  :substitutions:

  python3 -m pip install --extra-index-url https://artifacts.luxonis.com/artifactory/luxonis-python-snapshot-local/ depthai==|release| numpy==1.19.5 opencv-python==4.5.1.48


For additional information, please follow :ref:`Python API installation guide <Installation - Python>`

This example also requires MobilenetSDD blob (:code:`mobilenet.blob` file) to work - you can download it from
`here <https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/mobilenet-ssd_openvino_2021.2_5shave.blob>`__

Source code
###########

.. literalinclude:: ../../../examples/15_rgb_mobilenet_4k.py
   :language: python
   :linenos:

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/develop/examples/15_rgb_mobilenet_4k.py>`__

.. include::  /includes/footer-short.rst
