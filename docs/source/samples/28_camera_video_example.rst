28 - Camera video high resolution
=================================

This example shows how to use high resolution video at low latency. Compared to :ref:`01 - RGB Preview`, this demo outputs NV12 frames whereas
preview frames are BGR and are not suited for larger resoulution (eg. 2000x1000). Preview is more suitable for either NN or visualization purposes.

Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/-sTQLEVvO38" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>

Setup
#####

.. include::  /includes/install_from_pypi.rst

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/main/examples/28_camera_video_example.py>`__

.. literalinclude:: ../../../examples/28_camera_video_example.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
