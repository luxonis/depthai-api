25 - System information
=========================

This example shows how to get system information (memory usage, cpu usage and temperature) from the board.

Setup
#####

Please run the following command to install the required dependencies


.. code-block:: bash
  :substitutions:

  python3 -m pip install --extra-index-url https://artifacts.luxonis.com/artifactory/luxonis-python-snapshot-local/ depthai==|release| opencv-python==4.5.1.48


For additional information, please follow :ref:`Python API installation guide <Installation - Python>`

Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/develop/examples/25_system_information.py>`__

.. literalinclude:: ../../../examples/25_system_information.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst