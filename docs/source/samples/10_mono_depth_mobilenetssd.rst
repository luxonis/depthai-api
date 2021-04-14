10 - Mono & MobilenetSSD & Depth
================================

This example shows how to run MobileNetv2SSD on the left grayscale camera in parallel with running
the disparity depth results, displaying both the depth map and the right grayscale stream, with the
bounding box from the neural network overlaid.

Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/aCT0CRXx1qI" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>

Setup
#####

.. include::  /includes/install_from_pypi.rst

This example also requires MobilenetSDD blob (:code:`mobilenet-ssd_openvino_2021.2_6shave.blob` file) to work - you can download it from
`here <https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/mobilenet-ssd_openvino_2021.2_6shave.blob>`__

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/main/examples/10_mono_depth_mobilenetssd.py>`__

.. literalinclude:: ../../../examples/10_mono_depth_mobilenetssd.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
