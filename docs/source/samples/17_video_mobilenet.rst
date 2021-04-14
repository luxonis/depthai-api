17 - Video & MobilenetSSD
=========================

This example shows how to MobileNetv2SSD on the RGB input frame, which is read from the specified file,
and not from the RGB camera, and how to display both the RGB
frame and the metadata results from the MobileNetv2SSD on the frame.
DepthAI is used here only as a processing unit

Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/4DVzHw1f8p8" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>


Setup
#####

.. include::  /includes/install_from_pypi.rst

This example also requires MobilenetSDD blob (:code:`mobilenet-ssd_openvino_2021.2_8shave.blob` file) and prerecorded video
(:code:`construction_vest.mp4` file) to work - you can download them
here: `mobilenet-ssd_openvino_2021.2_8shave.blob <https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/mobilenet-ssd_openvino_2021.2_8shave.blob>`__
and `construction_vest.mp4 <https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/construction_vest.mp4>`__

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/main/examples/17_video_mobilenet.py>`__

.. literalinclude:: ../../../examples/17_video_mobilenet.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
