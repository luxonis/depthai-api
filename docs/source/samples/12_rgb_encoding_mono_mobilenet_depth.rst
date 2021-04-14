12 - RGB Encoding & Mono with MobilenetSSD & Depth
==================================================

This example shows how to configure the depthai video encoder in h.265 format to encode the RGB camera
input at Full-HD resolution at 30FPS, and transfers the encoded video over XLINK to the host,
saving it to disk as a video file. At the same time, a MobileNetv2SSD network is ran on the
frames from right grayscale camera, while the application also displays the depth map produced by both
of the grayscale cameras. Note that disparity is used in this case, as it colorizes in a more
intuitive way.

Pressing Ctrl+C will stop the recording and then convert it using ffmpeg into an mp4 to make it
playable. Note that ffmpeg will need to be installed and runnable for the conversion to mp4 to succeed.

Be careful, this example saves encoded video to your host storage. So if you leave it running,
you could fill up your storage on your host.

Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/3sijxVDVFY8" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>

Setup
#####

.. include::  /includes/install_from_pypi.rst

This example also requires MobilenetSDD blob (:code:`mobilenet-ssd_openvino_2021.2_6shave.blob` file) to work - you can download it from
`here <https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/mobilenet-ssd_openvino_2021.2_6shave.blob>`__

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/main/examples/12_rgb_encoding_mono_mobilenet_depth.py>`__

.. literalinclude:: ../../../examples/12_rgb_encoding_mono_mobilenet_depth.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
