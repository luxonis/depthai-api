Installation - Python
=====================

Instructions for installing, upgrading, and using the DepthAI Python API.

Supported Platforms
###################

The DepthAI Gen2 API python module is prebuilt for **Ubuntu**, **macOS** and **Windows**.
For other operating systems and/or Python versions, DepthAI can be :ref:`built from source <Other installation methods>`.

Installing system dependencies
##############################

A couple of basic system dependencies are required to run the DepthAI library. Most of them should be already installed
in most of the systems, but in case they are not, we prepared :download:`an install script </_static/install_dependencies.sh>`
that will make sure all dependencies are installed, along with convenient development/programming tools.
There are also video guides available for macOS (`here <https://youtu.be/0RGmmjed3Hc>`__), Raspberry Pi (`here <https://youtu.be/BpUMT-xqwqE>`__),
Ubuntu (`here <https://youtu.be/QXeXMaxj4cM>`__), and Windows 10 (`here <https://youtu.be/ekopKJfcWiE>`__).

macOS
*****

.. code-block:: bash

  bash -c "$(curl -fL http://docs.luxonis.com/_static/install_dependencies.sh)"

Close and re-open the terminal window after this command.

The script also works on M1 Macs, Homebrew being installed under Rosetta 2, as some Python packages are still missing native M1 support.
In case you already have Homebrew installed natively and things don't work, see `here <https://github.com/luxonis/depthai/issues/299#issuecomment-757110966>`__
for some additional troubleshooting steps.

Note that if the video streaming window does not appear consider running the
following:

.. code-block:: bash

    python3 -m pip install opencv-python --force-reinstall --no-cache-dir

See the `Video preview window fails to appear on macOS <https://discuss.luxonis.com/d/95-video-preview-window-fails-to-appear-on-macos>`_ thread on our forum for more information.

Raspberry Pi OS
***************

.. code-block:: bash

  sudo curl -fL http://docs.luxonis.com/_static/install_dependencies.sh | bash

Ubuntu
******

.. code-block:: bash

  sudo wget -qO- http://docs.luxonis.com/_static/install_dependencies.sh | bash

Windows
*******

- Right click on Start
- Choose Windows PowerShell (Admin)
- Install Chocolatey package manager (similar to Homebrew for macOS):

.. code-block:: bash

  Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

- Close the PowerShell and then re-open another PowerShell (Admin) by repeating the first two steps.
- Install Python and PyCharm

.. code-block:: bash

  choco install cmake git python pycharm-community -y

Enabling the USB device (only on Linux)
#######################################

Since the DepthAI is a USB device, in order to communicate with it on the systems that use :code:`udev` tool, you
need to add the udev rules in order to make the device accessible.

The following command will add a new udev rule to your system

.. code-block:: bash

  echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
  sudo udevadm control --reload-rules && sudo udevadm trigger

Install using pip
#################

Our packages are available to download using our `Artifactory server <https://artifacts.luxonis.com/artifactory/luxonis-python-snapshot-local/>`__.
These are built for every commit in the `depthai-python <https://github.com/luxonis/depthai-python/tree/gen2_develop>`__ repository and are suffixed
with a commit SHA.

Note that we recommend installing the dependencies in a virtual environment, so that they don't interfere with other Python
tools/environments on your system.

- For development machines like Mac/Windows/Ubuntu/etc., we recommend the `PyCharm <https://www.jetbrains.com/pycharm/>`__ IDE, as it automatically makes/manages virtual environments for you, along with a bunch of other benefits.  Alternatively, :code:`conda`, :code:`pipenv`, or :code:`virtualenv` could be used directly (and/or with your preferred IDE).
- For installations on resource-constrained systems, such as the Raspberry Pi or other small Linux systems, we recommend :code:`conda`, :code:`pipenv`, or :code:`virtualenv`.  To set up a virtual environment with :code:`virtualenv`, run

  .. code-block:: bash

    virtualenv venv
    source venv/bin/activate

Using a virtual environment (or system-wide, if you prefer), run the following to install the DepthAI using pip:

#. Pick the preferred commit from `commit list <https://github.com/luxonis/depthai-python/commits/gen2_develop>`__

#. Upgrade pip

  .. code-block:: bash

    python3 -m pip install -U pip

#. Install DepthAI Gen2 API, adding commit SHA at the end of a package name, in form of :code:`depthai==0.0.2.1+<sha>`

  .. code-block:: bash
    :substitutions:

    python3 -m pip install --extra-index-url https://artifacts.luxonis.com/artifactory/luxonis-python-snapshot-local/ depthai==|release|

For other installation options, see :ref:`other installation options <Other installation methods>`.

Test installation
#################

We have `a set of examples <https://github.com/luxonis/depthai-python/tree/gen2_develop/examples>`__ that should help you verify if your setup was correct.

First, clone the `depthai-python <https://github.com/luxonis/depthai-python/tree/gen2_develop>`__ repository and change directory into this repo:

.. code-block:: bash

  git clone https://github.com/luxonis/depthai-python.git --branch gen2_develop
  cd depthai-python

Now, run the :code:`01_rgb_preview.py` script from within :code`examples` directory to make sure everything is working:

.. code-block:: bash

  python3 examples/01_rgb_preview.py

If all goes well a small window video display will appear with color camera preview


.. warning::

  Some of the examples needs additional setup to be ran. Please be sure to follow `setup instructions in README.md <https://github.com/luxonis/depthai-python/tree/gen2_develop/examples#depthai-python-examples>`__
  to run different examples

Other installation methods
##########################

To get the latest features from our source code, you can go ahead and compile depthai package manually.

Dependencies to build from source
*********************************

- CMake > 3.2.0
- Generation tool (Ninja, make, ...)
- C/C++ compiler
- libusb1 development package

.. _raspbian:

Ubuntu, Raspberry Pi OS, ... (Debian based systems)
---------------------------------------------------

On Debian based systems (Raspberry Pi OS, Ubuntu, ...) these can be acquired by running:

.. code-block:: bash

  sudo apt-get -y install cmake libusb-1.0-0-dev build-essential

macOS (Mac OS X)
----------------

Assuming a stock Mac OS X install, `depthai-python <https://github.com/luxonis/depthai-python/tree/gen2_develop>`__ library needs following dependencies

- Homebrew (If it's not installed already)

  .. code-block:: bash

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

- Python, libusb, CMake, wget

  .. code-block:: bash

      brew install coreutils python3 cmake libusb wget

And now you're ready to clone the `depthai-python gen2_develop branch <https://github.com/luxonis/depthai-python/tree/gen2_develop>`__ from Github and build it for Mac OS X.

Using/Testing a Specific Branch/PR
**********************************

From time to time, it may be of interest to use a specific branch.  This may occur, for example,
because we have listened to your feature request and implemented a quick implementation in a branch.
Or it could be to get early access to a feature that is soaking in for stability purposes before being merged.

So when working in the `depthai-python <https://github.com/luxonis/depthai-python/tree/gen2_develop>`__ repository, using a branch can be accomplished
with the following commands.

Prior to running the following, you can either clone the repository independently
(for not over-writing any of your local changes) or simply do a :code:`git pull` first.

.. code-block:: bash

  git checkout <branch>
  git submodule update --init --recursive
  python3 setup.py develop

Install from source
*******************

If desired, you can also install the package from the source code itself - it will allow you to make the changes
to the API and see them live in action.

To do so, first download the repository and then add the package to your python interpreter in development mode

.. code-block:: bash

  git clone https://github.com/luxonis/depthai-python.git --branch gen2_develop
  cd depthai-python
  git submodule update --init --recursive
  python3 setup.py develop  # you may need to add sudo if using system interpreter instead of virtual environment
