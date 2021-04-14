14.1 - Color Camera Control
===========================

This example shows how to controll the device-side crop and camera triggers.
An output is a displayed RGB cropped frame, that can be manipulated using the following keys:

#. `a` will move the crop left
#. `d` will move the crop right
#. `w` will move the crop up
#. `s` will move the crop down
#. `c` will trigger a `still` event, causing the current frame to be captured and sent over `still` output from camera node
#. `t` will trigger autofocus
#. `f` will trigger autofocus continuously
#. `e` will trigger autoexposure
#. `i` and `o` will decrease/increase the exposure time
#. `k` and `l` will decrease/increase the sensitivity iso
#. `,` and `.` will decrease/increase the focus range

Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/httOxe2LAkI" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>

Setup
#####

.. include::  /includes/install_from_pypi.rst

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/main/examples/14_1_color_camera_control.py>`__

.. literalinclude:: ../../../examples/14_1_color_camera_control.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
