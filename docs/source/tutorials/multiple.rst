Multiple DepthAI per Host
=========================

Learn how to discover DepthAI devices connected to your system, and use them individually.

.. image:: /_static/images/tutorials/multiple/setup.jpg
  :alt: face

Shown on the left is Luxonis `uAI (BW1093) <https://shop.luxonis.com/products/bw1093>`__ which is actually plugged into
a `Raspberry Pi Compute Module Edition (BW1097) <https://shop.luxonis.com/products/depthai-rpi-compute-module-edition>`__.

So in this case, everything is running on the (single) Raspberry Pi 3B+ which is in the back of the BW1097.

Dependencies
############

You have already set up the Python API on your system (if you have a Raspberry Pi Compute Module it came pre-setup).
See :ref:`here <Python API Reference>` if you have not yet installed the DepthAI Python API on your system.

Discover DepthAI-USB Port Mapping
#################################

The DepthAI multi-device support is currently done by selecting the device mx_id (serial number) of a connected DepthAI
device.

If you'd like to associate a given DepthAI device with specific code (e.g. neural model) to be run on it, it is recommended
to plug in one device at a time, and then use the following code to determine which device is on which port:

.. code-block:: python

  import depthai
  for device in depthai.Device.getAllAvailableDevices():
      print(f"{device.getMxId()} {device.state}")

Example results for 2x DepthAI on a system:

.. code-block::

  14442C10D13EABCE00 XLinkDeviceState.X_LINK_UNBOOTED
  14442C1071659ACD00 XLinkDeviceState.X_LINK_UNBOOTED

Selecting a Specific DepthAI device to be used.
###############################################

From the Detected devices(s) above, use the following code to select the device you would like to use with your pipeline.
For example, if the first device is desirable from above use the following code:

.. code-block:: python

  device = depthai.Device.getDeviceByMxId("14442C10D13EABCE00")

And you can use this code as a basis for your own use cases, such that you can run differing neural models
on different DepthAI/uAI models.

Now use as many DepthAI devices as you need!

And since DepthAI does all the heavy lifting, you can usually use quite a
few of them with very little burden to the host.

.. include::  /includes/footer-short.rst
