06 - RGB Full Resolution Saver
==============================

This example does its best to save full-resolution 3840x2160 .png files as fast at it can from the
RGB sensor. It serves as an example of recording high resolution to disk for the purposes of
high-resolution ground-truth data. We also recently added the options to save isp - YUV420p
uncompressed frames, processed by ISP, and raw - BayerRG (R_Gr_Gb_B), as read from sensor,
10-bit packed. See here for the pull request on this capability.

Be careful, this example saves full resolution .png pictures to your host storage. So if you leave
them running, you could fill up your storage on your host.

Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/DJYzj7jwyY4" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
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

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/gen2_develop/examples/06_rgb_full_resolution_saver.py>`__

.. literalinclude:: ../../../examples/06_rgb_full_resolution_saver.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
