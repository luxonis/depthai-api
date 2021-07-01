.. _components_pipeline:

Pipeline
========

Pipeline is a collection of :ref:`nodes <Nodes>` and links between them. This flow provides extensive flexibility that users get for their
DepthAI device.


Pipeline first steps
####################

To get DepthAI up and running, one has to define a pipeline, populate it with nodes, configure the nodes and link them together. After that, the pipeline
can be loaded onto the :ref:`Device` and be started.

.. code-block:: python

  pipeline = depthai.Pipeline()

  # Create nodes, configure them and link them together

  # Upload the pipeline to the device
  with depthai.Device(pipeline) as device:
    # Start the pipeline that is now on the device
    device.startPipeline()

    # Set input/output queues to configure device/host communication through the XLink...

Using multiple devices
######################

If user has multiple DepthAI devices, each device can run a separate pipeline or the same pipeline
(`demo here <https://github.com/luxonis/depthai-experiments/tree/master/gen2-multiple-devices>`__). To use different pipeline for each device,
you can create multiple pipelines and pass the desired pipeline to the desired device on initialization.

Specifying OpenVINO version
###########################

When using a NN blob that was not compiled with the latest OpenVINO (that DepthAI supports), you have to specify the OpenVINO version of the pipeline.
The reason behind this is that OpenVINO doesn't provide version inside the blob.

.. code-block:: python

  pipeline = depthai.Pipeline()
  # Set the correct version:
  pipeline.setOpenVINOVersion(depthai.OpenVINO.Version.VERSION_2021_4)

How to place it
###############

.. tabs::

  .. code-tab:: py

    pipeline = dai.Pipeline()

  .. code-tab:: c++

    dai::Pipeline pipeline;

Reference
#########

.. tabs::

  .. tab:: Python

    .. autoclass:: depthai.Pipeline
      :members:
      :inherited-members:
      :noindex:

  .. tab:: C++

    .. doxygenclass:: dai::Pipeline
      :project: depthai-core
      :members:
      :private-members:
      :undoc-members:

.. include::  ../includes/footer-short.rst
