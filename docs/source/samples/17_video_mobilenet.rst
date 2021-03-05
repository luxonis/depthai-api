17 - Video & MobilenetSSD
=========================

This example shows how to MobileNetv2SSD on the RGB input frame, which is read from the specified file,
and not from the RGB camera, and how to display both the RGB
frame and the metadata results from the MobileNetv2SSD on the frame.
DepthAI is used here only as a processing unit

Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://www.youtube.com/embed/T8kipWWdq98" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>


Setup
#####

Please run the following command to install the required dependencies

.. code-block:: bash
  :substitutions:

  python3 -m pip install --extra-index-url https://artifacts.luxonis.com/artifactory/luxonis-python-snapshot-local/ depthai==|release| numpy==1.19.5 opencv-python==4.5.1.48


For additional information, please follow :ref:`Python API installation guide <Installation - Python>`

This example also requires MobilenetSDD blob (:code:`mobilenet.blob` file) and prerecorded video
(:code:`construction_vest.mp4` file) to work - you can download them
here: `mobilenet.blob <https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/mobilenet-ssd_openvino_2021.2_6shave.blob>`__
and `construction_vest.mp4 <https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/construction_vest.mp4>`__

Source code
###########

.. literalinclude:: ../../../examples/17_video_mobilenet.py
   :language: python
   :linenos:

Also `available on GitHub <https://github.com/luxonis/depthai-python/blob/develop/examples/17_video_mobilenet.py>`__

.. include::  /includes/footer-short.rst
