Local OpenVINO Model Conversion
===============================

In this tutorial, you'll learn how to convert OpenVINO IR models into the format required to run on DepthAI, even on a
low-powered Raspberry Pi. I'll introduce you to the OpenVINO toolset, the Open Model Zoo (where we'll download the
`face-detection-retail-0004 <https://github.com/opencv/open_model_zoo/blob/2019_R3/models/intel/face-detection-retail-0004/description/face-detection-retail-0004.md>`__
model), and show you how to generate the files needed to run model inference on your DepthAI board.

.. image:: /_static/images/tutorials/local_convert_openvino/face.png
  :alt: face

Haven't heard of OpenVINO or the Open Model Zoo? I'll start with a quick introduction of why we need these tools.

What is OpenVINO?
#################

Under-the-hood, DepthAI uses the Intel tecnnology to perform high-speed model inference. However, you can't just dump
your neural net into the chip and get high-performance for free. That's where
`OpenVINO <https://docs.openvinotoolkit.org/>`__ comes in. OpenVINO is a free toolkit that converts a deep learning
model into a format that runs on Intel Hardware. Once the model is converted, it's common to see Frames Per Second
(FPS) improve by 25x or more. Are a couple of small steps worth a 25x FPS increase? Often, the answer is yes!

What is the Open Model Zoo?
###########################

The `Open Model Zoo <https://github.com/opencv/open_model_zoo>`__ is a library of freely-available pre-trained models.
The Zoo also contains scripts for downloading those models into a compile-ready format to run on DepthAI.

DepthAI is able to run many of the object detection models in the Zoo.

Install OpenVINO
################

.. warning::

  If you have OpenVINO installed or want to follow `official installation <https://software.intel.com/content/www/us/en/develop/tools/openvino-toolkit.html>`__, **skip this step**.

  Please note that the following install instructions are for **Ubuntu 18.04** OS, if you intend to use other OS, follow
  the official OpenVINO installation


DepthAI requires OpenVINO version :code:`2020.1`. Let's get a package for our OS and meeting this version with the following command:

.. code-block:: bash

  apt-get update
  apt-get install -y software-properties-common
  add-apt-repository -y ppa:deadsnakes/ppa
  apt-get update
  apt-get install -y wget pciutils python3.8 libpng-dev libcairo2-dev libpango1.0-dev libglib2.0-dev libgtk2.0-dev libswscale-dev libavcodec-dev libavformat-dev
  cd
  mkdir openvino_install && cd openvino_install
  wget http://registrationcenter-download.intel.com/akdlm/irc_nas/16345/l_openvino_toolkit_p_2020.1.023.tgz
  tar --strip-components=1 -zxvf l_openvino_toolkit_p_2020.1.023.tgz
  ./install_openvino_dependencies.sh
  ./install.sh # when finished, you can go ahead and do "rm -r ~/openvino_install"

Now, first screen we'll wee is EULA, just hit :code:`Enter`, scroll through and type :code:`accept`.

Next one is agreement to Intel Software Improvement Program, it's not relevant so you can choose whether consent (:code:`1`)
or not (:code:`2`)

Next, you may see the Missing Prerequisites screen showing that :code:`Intel® Graphics Compute Runtime for OpenCL™ Driver is missing` - you can go ahead and ignore this warning.

Finally, we'll see the install summary - please verify that it has a correct location pointed out - :code:`/opt/intel`.
If all looks good, go ahead and proceed (:code:`1`). If the missing prerequisites screen appears again, feel free to skip it.

Let's verify that a correct version is installed on your host. Check your version by running the following from a terminal session:

.. code-block:: bash

  cat /opt/intel/openvino/inference_engine/version.txt

You should see output similar to:

.. code-block::

  Thu Jan 23 19:14:14 MSK 2020
  d349c3ba4a2508be72f413fa4dee92cc0e4bc0e1
  releases_2020_1_InferenceEngine_37988

Verify that you see :code:`releases_2020_1` in your output. If you do, move on. If you are on a different version,
goto the `OpenVINO site <https://docs.openvinotoolkit.org/2019_R3/index.html>`__ and download the :code:`2020.1` version for your OS:

.. image:: /_static/images/tutorials/local_convert_openvino/openvino_version.png
  :alt: face

Check if the Model Downloader is installed
##########################################

When installing OpenVINO, you can choose to perform a smaller install to save disk space. This custom install may not
include the model downloader script. Lets check if the downloader was installed. In a terminal session, type the following:

.. code-block:: bash

  find /opt/intel/ -iname downloader.py

**Move on if you see the output below**:

.. code-block:: bash

  /opt/intel/openvino_2020.1.023/deployment_tools/open_model_zoo/tools/downloader/downloader.py

**Didn't see any output?** Don't fret if :code:`downloader.py` isn't found. We'll install this below.

Install Open Model Zoo Downloader
*********************************

If the downloader tools weren't found, we'll install the tools by cloning the
`Open Model Zoo Repo <https://github.com/openvinotoolkit/open_model_zoo/blob/2020.1/tools/downloader/README.md>`__ and
installing the tool dependencies.

Start a terminal session and run the following commands in your terminal:

.. code-block:: bash

  apt-get install -y git curl
  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  python3 get-pip.py
  rm get-pip.py
  cd ~
  git clone https://github.com/opencv/open_model_zoo.git
  cd open_model_zoo
  git checkout tags/2020.1
  cd tools/downloader
  python3 -m pip install --user -r ./requirements.in

This clones the repo into a :code:`~/open_model_zoo` directory, checks out the required :code:`2020.1` version, and
installs the downloader dependencies.

Create an OPEN_MODEL_DOWNLOADER environment variable
####################################################

Typing the full path to :code:`downloader.py` can use a lot of keystrokes. In an effort to extend your keyboard life,
let's store the path to this script in an environment variable.

Run the following in your terminal:

.. code-block:: bash

  export OPEN_MODEL_DOWNLOADER='INSERT PATH TO YOUR downloader.py SCRIPT'

Where :code:`INSERT PATH TO YOUR downloader.py SCRIPT` can be found via:

.. code-block:: bash

  find /opt/intel/ -iname downloader.py
  find ~ -iname downloader.py

For example, if you installed :code:`open_model_zoo` yourself:

.. code-block:: bash

  export OPEN_MODEL_DOWNLOADER="$HOME/open_model_zoo/tools/downloader/downloader.py"

Download the face-detection-retail-0004 model
#############################################

We've installed everything we need to download models from the Open Model Zoo! We'll now use the
`Model Downloader <https://github.com/opencv/open_model_zoo/blob/2019_R3/tools/downloader/README.md>`__ to download the
:code:`face-detection-retail-0004` model files. Run the following in your terminal:

.. code-block:: bash

  $OPEN_MODEL_DOWNLOADER --name face-detection-retail-0004 --output_dir ~/open_model_zoo_downloads/

This will download the model files to :code:`~/open_model_zoo_downloads/`. Specifically, the model files we need are
located at:

.. code-block:: bash

  ~/open_model_zoo_downloads/intel/face-detection-retail-0004/FP16

You'll see two files within the directory:

.. code-block:: bash

  $ ls -lh
  total 1.3M
  -rw-r--r-- 1 root root 1.2M Jul 28 12:40 face-detection-retail-0004.bin
  -rw-r--r-- 1 root root 100K Jul 28 12:40 face-detection-retail-0004.xml

The model is in the OpenVINO Intermediate Representation (IR) format:

- :code:`face-detection-retail-0004.xml` - Describes the network topology
- :code:`face-detection-retail-0004.bin` - Contains the weights and biases binary data.

This means we are ready to compile the model for the MyriadX!

Compile the model
#################

The MyriadX chip used on our DepthAI board does not use the IR format files directly. Instead, we need to generate
:code:`face-detection-retail-0004.blob` using :code:`myriad_compile` command.

Locate myriad_compile
*********************

Let's find where :code:`myriad_compile` is located. In your terminal, run:

.. code-block:: bash

  find /opt/intel/ -iname myriad_compile

You should see the output similar to this

.. code-block:: bash

  find /opt/intel/ -iname myriad_compile
  /opt/intel/openvino_2020.1.023/deployment_tools/inference_engine/lib/intel64/myriad_compile

Since it's such a long path, let's store the :code:`myriad_compile` executable in an environment variable (just like
:code:`OPEN_MODEL_DOWNLOADER`):

.. code-block:: bash

  export MYRIAD_COMPILE=$(find /opt/intel/ -iname myriad_compile)

Activate OpenVINO environment
*****************************

In order to use :code:`myriad_compile` tool, we need to activate our OpenVINO environment.

First, let's find :code:`setupvars.sh` file

.. code-block:: bash

  find /opt/intel/ -name "setupvars.sh"
  /opt/intel/openvino_2020.1.023/opencv/setupvars.sh
  /opt/intel/openvino_2020.1.023/bin/setupvars.sh

We're interested in :code:`bin/setupvars.sh` file, so let's go ahead and source it to activate the environment:

.. code-block:: bash

  source /opt/intel/openvino_2020.1.023/bin/setupvars.sh
  [setupvars.sh] OpenVINO environment initialized

If you see :code:`[setupvars.sh] OpenVINO environment initialized` then your environment should be initialized correctly

Run myriad_compile
******************

.. code-block:: bash

  $MYRIAD_COMPILE -m ~/open_model_zoo_downloads/intel/face-detection-retail-0004/FP16/face-detection-retail-0004.xml -ip U8 -VPU_MYRIAD_PLATFORM VPU_MYRIAD_2480 -VPU_NUMBER_OF_SHAVES 4 -VPU_NUMBER_OF_CMX_SLICES 4

You should see:

.. code-block:: bash

  Inference Engine:
    API version ............ 2.1
    Build .................. 37988
    Description ....... API
  Done

Where's the blob file? It's located in the same folder as :code:`face-detection-retail-0004.xml`:

.. code-block:: bash

  ls -lh ~/open_model_zoo_downloads/intel/face-detection-retail-0004/FP16/
  total 2.6M
  -rw-r--r-- 1 root root 1.2M Jul 28 12:40 face-detection-retail-0004.bin
  -rw-r--r-- 1 root root 1.3M Jul 28 12:50 face-detection-retail-0004.blob
  -rw-r--r-- 1 root root 100K Jul 28 12:40 face-detection-retail-0004.xml

Run and display the model output
################################

With neural network :code:`blob` in place, we're ready to roll!
To verify that the model is running correctly, let's modify a bit the program we've created in :ref:`Hello World` tutorial

In particular, let's change the :code:`setBlobPath` invocation to load our model. **Remember to replace the paths to correct ones that you have!**

.. code-block:: diff

  - detection_nn.setBlobPath("/path/to/mobilenet-ssd.blob")
  - detection_nn.setBlobPath("/path/to/face-detection-retail-0004.blob")

And that's all!

You should see output annotated output similar to:

.. image:: /_static/images/tutorials/local_convert_openvino/face.png
  :alt: face

Reviewing the flow
##################

The flow we walked through works for other pre-trained object detection models in the Open Model Zoo:

#. Download the model:

    .. code-block:: bash

      $OPEN_MODEL_DOWNLOADER --name [INSERT MODEL NAME] --output_dir ~/open_model_zoo_downloads/

#. Create the MyriadX blob file:

    .. code-block:: bash

      $MYRIAD_COMPILE -m [INSERT PATH TO MODEL XML FILE] -ip U8 -VPU_MYRIAD_PLATFORM VPU_MYRIAD_2480 -VPU_NUMBER_OF_SHAVES 4 -VPU_NUMBER_OF_CMX_SLICES 4

#. Use this model in your script

You’re on your way! You can find the `complete code for this tutorial on GitHub. <https://github.com/luxonis/depthai-tutorials/blob/master/2-face-detection-retail/face-detection-retail-0004.py>`__

.. include::  /includes/footer-short.rst


