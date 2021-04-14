14.2 - Mono Camera Control
==========================

This example shows how to controll the device-side crop and camera triggers.
TWo output is a displayed mono cropped frame, that can be manipulated using the following keys:

#. `a` will move the crop left
#. `d` will move the crop right
#. `w` will move the crop up
#. `s` will move the crop down
#. `e` will trigger autoexposure
#. `i` and `o` will decrease/increase the exposure time
#. `k` and `l` will decrease/increase the sensitivity iso


Demo
####


Setup
#####

.. include::  /includes/install_from_pypi.rst

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/main/examples/14_2_mono_camera_control.py>`__

.. literalinclude:: ../../../examples/14_2_mono_camera_control.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
