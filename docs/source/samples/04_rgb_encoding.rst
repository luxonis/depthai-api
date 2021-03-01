04 - RGB Encoding
=================

This example shows how to configure the depthai video encoder in h.265 format to encode the RGB camera
input at 8MP/4K/2160p (3840x2160) at 30FPS (the maximum possible encoding resolultion possible for the
encoder, higher frame-rates are possible at lower resolutions, like 1440p at 60FPS), and transfers the
encoded video over XLINK to the host, saving it to disk as a video file.

Pressing Ctrl+C will stop the recording and then convert it using ffmpeg into an mp4 to make it
playable. Note that ffmpeg will need to be installed and runnable for the conversion to mp4 to succeed.

Be careful, this example saves encoded video to your host storage. So if you leave them running,
you could fill up your storage on your host.


Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/k_4t8h_7OWo" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>

Setup
#####

Please run the following command to install the required dependencies

.. code-block:: bash
  :substitutions:

  python3 -m pip install --extra-index-url https://artifacts.luxonis.com/artifactory/luxonis-python-snapshot-local/ depthai==|release| numpy==1.19.5 opencv-python==4.5.1.48


For additional information, please follow :ref:`Python API installation guide <Installation - Python>`

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/gen2_develop/examples/04_rgb_encoding.py>`__

.. literalinclude:: ../../../examples/04_rgb_encoding.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
