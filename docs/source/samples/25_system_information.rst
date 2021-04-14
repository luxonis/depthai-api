25 - System information
=======================

This example shows how to get system information (memory usage, cpu usage and temperature) from the board.

Demo
####

Example script output

.. code-block::

  Drr used / total - 0.13 / 414.80 MiB
  Cmx used / total - 2.24 / 2.50 MiB
  LeonCss heap used / total - 4.17 / 46.41 MiB
  LeonMss heap used / total - 2.87 / 27.58 MiB
  Chip temperature - average: 38.59, css: 39.81, mss: 37.71, upa0: 38.65, upa1: 38.18
  Cpu usage - Leon OS: 7.08%, Leon RT: 1.48 %
  ----------------------------------------
  Drr used / total - 0.13 / 414.80 MiB
  Cmx used / total - 2.24 / 2.50 MiB
  LeonCss heap used / total - 4.17 / 46.41 MiB
  LeonMss heap used / total - 2.87 / 27.58 MiB
  Chip temperature - average: 38.59, css: 39.58, mss: 37.94, upa0: 38.18, upa1: 38.65
  Cpu usage - Leon OS: 1.55%, Leon RT: 0.30 %
  ----------------------------------------
  Drr used / total - 0.13 / 414.80 MiB
  Cmx used / total - 2.24 / 2.50 MiB
  LeonCss heap used / total - 4.17 / 46.41 MiB
  LeonMss heap used / total - 2.87 / 27.58 MiB
  Chip temperature - average: 38.94, css: 40.04, mss: 38.18, upa0: 39.35, upa1: 38.18
  Cpu usage - Leon OS: 0.56%, Leon RT: 0.06 %
  ----------------------------------------
  Drr used / total - 0.13 / 414.80 MiB
  Cmx used / total - 2.24 / 2.50 MiB
  LeonCss heap used / total - 4.17 / 46.41 MiB
  LeonMss heap used / total - 2.87 / 27.58 MiB
  Chip temperature - average: 39.46, css: 40.28, mss: 38.88, upa0: 39.81, upa1: 38.88
  Cpu usage - Leon OS: 0.51%, Leon RT: 0.06 %
  ----------------------------------------


Setup
#####

.. include::  /includes/install_from_pypi.rst


Source code
###########

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/main/examples/25_system_information.py>`__

.. literalinclude:: ../../../examples/25_system_information.py
   :language: python
   :linenos:

.. include::  /includes/footer-short.rst
