.. _components_bootloader:

Bootloader
==========

Depthai bootloader is a small program which aids in booting and updating bootloader or depthai application packages.

To be able to run in standalone mode (without a host), the Depthai bootloader must be first flashed to the devices flash.

.. note::
    Only devices that have "embedded" SoM (System on Module) can be run in standalone mode. These are `embedded devices <https://docs.luxonis.com/projects/hardware/en/latest/#pure-embedded-design>`__; `LUX-ESP32 <https://docs.luxonis.com/projects/hardware/en/latest/pages/DM1092.html>`__ and `LUX-D-WIFI <https://docs.luxonis.com/projects/hardware/en/latest/pages/DM1098OBC.html>`__.

This step is required only once.

- Plug the USB cable into the device
- Flash the bootloader using :code:`DeviceBootloader::flashBootloader` (Check code snippet below)
- **If you have an older version of the depthai device**, you also need to disconnect the board and switch the boot mode GPIO to the following settings: BOOT[4:0] : 01000 (see attached images for reference). Reassemble the board afterwards

Once the device has the bootloader flashed, it will perform the same as before. Running pipelines with a host connected doesn’t require any changes.

Suggested workflow is to perform as much of development as possible with the host connected as the iteration cycle is greatly improved.

Once desired pipeline is created, use the following function to flash: :code:`DeviceBootloader::flash`

API
###

**DeviceBootloader** is a class to communicate with the bootloader. It is used to flash created :ref:`Pipeline`, depthai application package
or update the bootloader itself.

.. code-block: cpp

    std::tuple<bool, std::string> flash(std::function<void(float)> progressCb, Pipeline& pipeline);

    std::tuple<bool, std::string> flashDepthaiApplicationPackage(std::function<void(float)> progressCb, std::vector<uint8_t> package);

    std::tuple<bool, std::string> flashBootloader(std::function<void(float)> progressCb, std::string path = "");

progressCb parameter takes a callback function, which will be called each time an progress update occurs (rate limited to 1 second). This is mainly
used to inform the user of the current flashing progress.

DepthAI Application Package (.dap)
##################################

Depthai application package is a binary file format which stores sections of data. The purpose of this format is to be able to extract
individual sections and do OTA updates without requiring to update all data. Example: Between update 1 and 2 of users application,
Depthai firmware, Asset storage (50MiB neural network) and asset structure remained the same, but some additional processing nodes were added
to the pipeline. Instead of transferring the whole package only Pipeline description can be sent and updated.

Depthai application package (**.dap**) consists of:

- SBR (512B header which describes sections of data)
- Depthai device firmware (section “__firmware”)
- Pipeline description (section “pipeline”)
- Assets structure (section “assets”)
- Asset storage (section “asset_storage”)

Example
#######

Following section will show an example of: Flashing bootloader (needed only once) and flashing a created Pipeline “myExamplePipeline” to the device
(The example is written in Python, similar steps apply to C++)

#. **Flashing bootloader**

    .. code-block:: python

        import depthai as dai
        (f, bl) = dai.DeviceBootloader.getFirstAvailableDevice()
        bootloader = dai.DeviceBootloader(bl)
        progress = lambda p : print(f'Flashing progress: {p*100:.1f}%')
        bootloader.flashBootloader(progress)

    .. note::
        If you have an older version of the depthai device, make sure to switch GPIO BOOT mode settings (See image below for more details)

#. **Flashing created pipeline**

    .. code-block:: python

        import depthai as dai
        # ...
        # Create Pipeline 'myExamplePipeline'
        # ...
        (f, bl) = dai.DeviceBootloader.getFirstAvailableDevice()
        bootloader = dai.DeviceBootloader(bl)
        progress = lambda p : print(f'Flashing progress: {p*100:.1f}%')
        bootloader.flash(progress, myExamplePipeline)

GPIO boot settings
******************
Boot settings must be set as following: BOOT[4:0] : 01000 and GPIO58 (WAKEUP): 0. **This is only needed
for the older versions of the depthai devices, newer devices do not have this DIP switch.**

.. image:: /_static/images/components/boot-depthai.jpeg
    :alt: boot-depthai

.. include::  ../includes/footer-short.rst
