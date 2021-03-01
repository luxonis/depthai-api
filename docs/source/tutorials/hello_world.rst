Hello World
===========

Learn how to use the DepthAI Python API to display a color video stream.


Demo
####

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="//www.youtube.com/embed/puI57TaFCUM" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>

.. _hello_world_dependencies:

Dependencies
############

Let's get your development environment setup first. This tutorial uses:

- Python 3.6 (Ubuntu) or Python 3.7 (Raspbian).
- The DepthAI :ref:`Python API`
- The :code:`cv2` and :code:`numpy` Python modules.


Code Overview
#############

The :code:`depthai` Python module provides access to your board's 4K 60 Hz color camera.
We'll display a video stream from this camera to your desktop.
You can find the `complete source code for this tutorial on GitHub <https://github.com/luxonis/depthai-tutorials/tree/gen2/1-hello-world>`__.

File Setup
##########

Setup the following file structure on your computer:

.. code-block:: bash

  cd ~
  mkdir -p depthai-tutorials-practice/1-hello-world
  touch depthai-tutorials-practice/1-hello-world/hello_world.py
  cd depthai-tutorials-practice/1-hello-world

What's with the :code:`-practice` suffix in parent directory name? Our tutorials are available on GitHub
via the `depthai-tutorials <https://github.com/luxonis/depthai-tutorials>`__ repository.
We're appending :code:`-practice` so you can distinguish between your work and our finished
tutorials (should you choose to download those).


Install pip dependencies
########################

To display the DepthAI color video stream we need to import a small number of packages.
Download and install the requirements for this tutorial:

.. code-block:: bash

  python3 -m pip install numpy opencv-python depthai --user


Test your environment
#####################

Let's verify we're able to load all of our dependencies. Open the :code:`hello_world.py` file you
:ref:`created earlier <File Setup>` in your code editor. Copy and paste the following into :code:`hello_world.py`:


.. code-block:: python

  import numpy as np # numpy - manipulate the packet data returned by depthai
  import cv2 # opencv - display the video stream
  import depthai # access the camera and its data packets

Try running the script and ensure it executes without error:

.. code-block:: bash

  python3 hello_world.py

If you see the following error:

.. code-block::

  ModuleNotFoundError: No module named 'depthai'

...follow `these steps in our troubleshooting section <https://docs.luxonis.com/en/latest/pages/troubleshooting/#importerror-no-module-named-depthai'>`__.

Define a pipeline
#################

Any action from DepthAI, whether it's a neural inference or color camera output, require a **pipeline** to be defined,
including nodes and connections corresponding to our needs.

In this case, we want to see the frames from **color camera**, as well as a simple **neural network** to be ran on top of them.

Let's start off with an empty :class:`Pipeline` object

.. code-block:: python

  pipeline = depthai.Pipeline()

Now, first node we will add is a :class:`ColorCamera`. We will use the :code:`preview` output, resized to 300x300 to fit the
`mobilenet-ssd input size <https://docs.openvinotoolkit.org/latest/omz_models_public_mobilenet_ssd_mobilenet_ssd.html>`__ (which we will define later)

.. code-block:: python

  cam_rgb = pipeline.createColorCamera()
  cam_rgb.setPreviewSize(300, 300)
  cam_rgb.setInterleaved(False)

Up next, let's define a :class:`NeuralNetwork` node with `mobilenet-ssd network <https://docs.openvinotoolkit.org/latest/omz_models_public_mobilenet_ssd_moblenet_ssd.html>`__.
The blob file for this example can be found `here <https://github.com/luxonis/depthai-tutorials/raw/e37989e07a36a57ffef624b7aa8cf20ab493fa07/1-hello-world/mobilenet-ssd/mobilenet-ssd.blob>`__

.. code-block:: python

  detection_nn = pipeline.createNeuralNetwork()
  detection_nn.setBlobPath("/path/to/mobilenet-ssd.blob")

And now, let's connect a color camera :code:`preview` output to neural network input

.. code-block:: python

  cam_rgb.preview.link(detection_nn.input)

Finally, we want to receive both color camera frames and neural network inference results - as these are produced on the
device, they need to be transported to our machine (host). The communication between device and host is handled by :code:`XLink`,
and in our case, since we want to receive data from device to host, we will use :class:`XLinkOut` node

.. code-block:: python

  xout_rgb = pipeline.createXLinkOut()
  xout_rgb.setStreamName("rgb")
  cam_rgb.preview.link(xout_rgb.input)

  xout_nn = pipeline.createXLinkOut()
  xout_nn.setStreamName("nn")
  detection_nn.out.link(xout_nn.input)


Initialize the DepthAI Device
#############################

Having the pipeline defined, we can now initialize a device and start it

.. code-block:: python

  device = depthai.Device(pipeline)
  device.startPipeline()

.. note::

  By default, the DepthAI is accessed as a USB3 device. This comes with `several limitations <https://docs.luxonis.com/en/latest/pages/troubleshooting/#intermittent-connectivity-with-long-2-meter-usb3-cables>`__.

  If you'd like to communicate via USB2, being free from these but having a limited bandwidth, initialize the DepthAI with the following code

  .. code-block:: python

    device = depthai.Device(pipeline, True)



From this point on, the pipeline will be running on the device, producing results we requested. Let's grab them

Adding helpers
##############

As :class:`XLinkOut` nodes has been defined in the pipeline, we'll define now a host side output queues to access the
produced results

.. code-block:: python

  q_rgb = device.getOutputQueue("rgb")
  q_nn = device.getOutputQueue("nn")

These will fill up with results, so next thing to do is consume the results. We will need two placeholders - one
for rgb frame and one for nn results

.. code-block:: python

  frame = None
  bboxes = []

Also, due to neural network implementation details, bounding box coordinates in inference results are represented
as floats from <0..1> range - so relative to frame width/height (e.g. if image has 200px width and nn returned x_min
coordinate equal to 0.2, this means the actual (normalised) x_min coordinate is 40px).

That's why we need to define a helper function, :code:`frame_form`, that will convert these <0..1> values into actual
pixel positions

.. code-block:: python

  def frame_norm(frame, bbox):
      return (np.array(bbox) * np.array([*frame.shape[:2], *frame.shape[:2]])[::-1]).astype(int)

Consuming the results
#####################

Having everything prepared, we are ready to start out main program loop

.. code-block:: python

  while True:
    # ...

Now, inside this loop, first thing to do is fetching latest results from both nn node and color camera

.. code-block:: python

  in_rgb = q_rgb.tryGet()
  in_nn = q_nn.tryGet()

The :code:`tryGet` method returns either the latest result or :code:`None` if the queue is empty.

Results, both from rgb camera or neural network, will be delivered as 1D arrays, so both of them will require transformations
to be useful for display (we have already defined one of the transformations needed - the :code:`frame_norm` function)

First up, if we receive a frame from rgb camera, we need to convert it from 1D array into HWC form (HWC stands for
Height Width Channels, so 3D array, with first dimension being width, second height, and third the color channel)

.. code-block:: python

  if in_rgb is not None:
      shape = (3, in_rgb.getHeight(), in_rgb.getWidth())
      frame = in_rgb.getData().reshape(shape).transpose(1, 2, 0).astype(np.uint8)
      frame = np.ascontiguousarray(frame)

Second, the neural network results will also need transformations. These are also returned as a 1D array, but this time
the array has a fixed size (constant, no matter how many results the neural network has actually produced).
Actual results in array are followed with :code:`-1` and then filled to meet the fixed size with :code:`0`.
One results has 7 fields, each being respectively :code:`image_id, label, confidence, x_min, y_min, x_max, y_max`.
We will want only the last four values (being the bounding box), but we'll also filter out the ones which :code:`confidence`
is below a certain threshold - it can be anywhere between <0..1>, and for this example we will use :code:`0.8` threshold

.. code-block:: python

  if in_nn is not None:
      bboxes = np.array(in_nn.getFirstLayerFp16())
      bboxes = bboxes[:np.where(bboxes == -1)[0][0]]
      bboxes = bboxes.reshape((bboxes.size // 7, 7))
      bboxes = bboxes[bboxes[:, 2] > 0.8][:, 3:7]

To better understand this flow, let's take an example. Let's assume the :code:`np.array(in_nn.getFirstLayerFp16())` returns the following array

.. code-block:: python

  [0, 15, 0.99023438, 0.45556641, 0.34399414  0.88037109, 0.9921875, 0, 15, 0.98828125, 0.03076172, 0.23388672, 0.60205078, 1.0078125, -1, 0, 0, 0, ...]

First operation, :code:`bboxes[:np.where(bboxes == -1)[0][0]]`, removes the trailing zeros from the array, so now the bbox array will look like this

.. code-block:: python

  [0, 15, 0.99023438, 0.45556641, 0.34399414  0.88037109, 0.9921875, 0, 15, 0.98828125, 0.03076172, 0.23388672, 0.60205078, 1.0078125]

Second one - :code:`bboxes.reshape((bboxes.size // 7, 7))`, reshapes the 1D array into 2D array - where each row is a separate result

.. code-block:: python

  [
    [0, 15, 0.99023438, 0.45556641, 0.34399414  0.88037109, 0.9921875],
    [0, 15, 0.98828125, 0.03076172, 0.23388672, 0.60205078, 1.0078125]
  ]

Last one - :code:`bboxes = bboxes[bboxes[:, 2] > 0.8][:, 3:7]` - will filter the results based on the confidence column (3rd one, with index :code:`2`)
to be above a defined threshold (:code:`0.8`) - and from these results, it will only take the last 4 columns being the bounding boxes.
Since both our results have a very high confidence (:code:`0.99023438` and :code:`0.98828125` respectively), they won't be filtered, and the final
array will look like this

.. code-block:: python

  [
    [0.45556641, 0.34399414  0.88037109, 0.9921875],
    [0.03076172, 0.23388672, 0.60205078, 1.0078125]
  ]

Display the results
###################

Up to this point, we have all our results consumed from the DepthaI device, and only thing left is to actually display them.

.. code-block:: python

  if frame is not None:
      for raw_bbox in bboxes:
          bbox = frame_norm(frame, raw_bbox)
          cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
      cv2.imshow("preview", frame)

You can see here the usage of :code:`frame_norm` we defined earlier for bounding box coordinates normalization.
By using :code:`cv2.rectangle` we draw a rectangle on the rgb frame as an indicator where the face position is, and then
we display the frame using :code:`cv2.imshow`

Finally, we add a way to terminate our program (as it's running inside an infinite loop). We will use :code:`cv2.waitKey`
method, that waits for a key to be pressed by user - in our case, we want to break out of the loop when user presses :code:`q` key

Running the example
###################

Putting it all together, only thing left to do is to run the file we've prepared in this tutorial and see the results

.. code-block:: bash

  python3 hello_world.py

You're on your way! You can find the `complete code for this tutorial on GitHub <https://github.com/luxonis/depthai-tutorials/blob/gen2/1-hello-world/hello_world.py>`__.

.. include::  /includes/footer-short.rst
