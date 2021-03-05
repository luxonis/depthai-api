14 - Color Camera Control
=========================

This example shows how to controll the device-side crop and camera triggers.
An output is a displayed RGB cropped frame, that can be manipulated using the following keys:

#. `a` will move the crop left
#. `d` will move the crop right
#. `w` will move the crop up
#. `s` will move the crop down
#. `c` will trigger a `still` event, causing the current frame to be captured and sent over `still` output from camera node

Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/httOxe2LAkI" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
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

.. literalinclude:: ../../../examples/14_color_camera_control.py
   :language: python
   :linenos:

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/develop/examples/14_color_camera_control.py>`__

.. include::  /includes/footer-short.rst
