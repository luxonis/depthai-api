16 - Device Queue Event
=======================

This example shows how to use :code:`getQueueEvent` function in order to be notified when one of
the packets from selected streams arrive

Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/QsFGPRX5fhw" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>


Setup
#####

Please run the following command to install the required dependencies

.. code-block:: bash
  :substitutions:

  python3 -m pip install depthai==|pypi_release| numpy==1.19.5 opencv-python==4.5.1.48


For additional information, please follow :ref:`Python API installation guide <Installation - Python>`

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/main/examples/16_device_queue_event.py>`__

.. literalinclude:: ../../../examples/16_device_queue_event.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
