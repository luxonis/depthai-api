13 - Encoding Max Limit
=====================

This example shows how to set up the encoder node to encode the RGB camera and both grayscale cameras
(of DepthAI/OAK-D) at the same time, having all encoder parameters set to maximum quality and FPS.
The RGB is set to 4K (3840x2160) and the grayscale are set to 1280x720 each, all at 30FPS.
Each encoded video stream is transferred over XLINK and saved to a respective file.

Pressing Ctrl+C will stop the recording and then convert it using ffmpeg into an mp4 to make it
playable. Note that ffmpeg will need to be installed and runnable for the conversion to mp4 to succeed.

Be careful, this example saves encoded video to your host storage. So if you leave them running,
you could fill up your storage on your host.

Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/myqmcSFq-i0" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
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

.. literalinclude:: ../../../examples/13_encoding_max_limit.py
   :language: python
   :linenos:

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/develop/examples/13_encoding_max_limit.py>`__

.. include::  /includes/footer-short.rst
