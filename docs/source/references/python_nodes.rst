.. class:: XLinkIn
  :canonical: depthai.XLinkIn

  Represents an XLink stream of data from host into device

  **Outputs**

  .. attribute:: out

    Output where the data received from the host is being sent

  **Methods**

  .. function:: setStreamName(name: string)

    Sets the stream name, needed for :func:`getInputQueue` to transfer data to it.

  .. function:: setMaxDataSize(maxDataSize: int)

    Maximum data size of a message to be allowed to go through the stream

  .. function:: setNumFrames(numFrames: int)

    Sets the stream buffer size, determining how many frames can be stored before sending to the connected node


.. class:: XLinkOut
  :canonical: depthai.XLinkOut

  Represents an XLink stream of data from device into host

  **Inputs**

  .. attribute:: input

    Input which receives the data and send it to host

  .. function:: setStreamName(name: string)

    Sets the stream name, needed for :func:`getOutputQueue` to transfer data from it.

  .. function:: setFpsLimit(fps: float)

    Limits the stream throughput


.. class:: ColorCamera
  :canonical: depthai.ColorCamera

  Represents an XLink stream of data from host into device

  **Inputs**

  .. attribute:: inputConfig

    Linkable to :class:`ImageManipConfig`, allowing to modify crop area, horizontal flip, frame datatype etc.

  .. attribute:: inputControl

    Linkable to :class:`CameraControl`, allowing to send signals to the camera, e.g. to capture a still image

  **Outputs**

  .. attribute:: video

    Color camera video stream NV12-encoded (YUV420, UV plane interleaved) output, suitable for VideoEncoder

  .. attribute:: preview

    Color camera video stream scaled to the preview size, set using :func:`setPreviewSize`

  .. attribute:: still

    Color camera output, NV12-encoded (YUV420, UV plane interleaved), captured when "take still" command is sent
    from :attr:`inputControl` input

  **Methods**

  .. function:: setBoardSocket(boardSocket: CameraBoardSocket)

    Assigns the camera socket to the node

  .. function:: getBoardSocket() -> CameraBoardSocket

    Returns the assigned board socket

  .. function:: setColorOrder(colorOrder: ColorCameraProperties.ColorOrder)

    Sets the color order of the frame

  .. function:: getColorOrder() -> ColorCameraProperties.ColorOrder

    Returns the color order of the frame

  .. function:: setFp16(fp16: bool)

    Forces the frame values to be in FP16 format

  .. function:: getFp16() -> bool

    Returns information if the output values were forced to be in FP16 format

  .. function:: setFps(fps: float)

    Limits the FPS of the node, allowing e.g. to decrease the amount of frames being produced by this node

  .. function:: getFps() -> float

    Returns the current FPS limit

  .. function:: setPreviewSize(width: int, height: int)

    Sets the desired preview dimensions, available as :attr:`preview` output

  .. function:: getPreviewSize() -> Tuple[int, int]

    Returns the preview dimensions previously set using :func:`setPreviewSize`

  .. function:: getPreviewWidth() -> int

    Returns width of the preview previously set using :func:`setPreviewSize`

  .. function:: getPreviewHeight() -> int

    Returns height of the preview previously set using :func:`setPreviewSize`

  .. function:: setVideoSize(width: int, height: int)

    Sets the desired video dimensions, available as :attr:`video` output

  .. function:: getVideoSize() -> Tuple[int, int]

    Returns the video dimensions previously set using :func:`setVideoSize`

  .. function:: getVideoWidth() -> int

    Returns width of the video previously set using :func:`setVideoSize`

  .. function:: getVideoHeight() -> int

    Returns height of the video previously set using :func:`setVideoSize`

  .. function:: setStillSize()

    Sets the desired image dimensions produced by :attr:`still` output

  .. function:: getStillSize()

    Returns the frame dimensions previously set using :func:`setStillSize`

  .. function:: getStillWidth()

    Returns width of the frame previously set using :func:`setStillSize`

  .. function:: getStillHeight()

    Returns height of the frame previously set using :func:`setStillSize`

  .. function:: setResolution(resolution: ColorCameraProperties.SensorResolution)

    Sets the camera sensor resolution, determining the maximum resolution that can be obtained from this node

  .. function:: getResolution() -> ColorCameraProperties.SensorResolution

    Returns camera resolution previously set using :func:`setResolution`

  .. function:: getResolutionSize() -> Tuple[int, int]

    Returns the sensor resolution dimensions

  .. function:: getResolutionWidth() -> int

    Returns the sensor resolution width

  .. function:: getResolutionHeight() -> int

    Returns the sensor resolution height

  .. function:: sensorCenterCrop()

    Enables center cropping from the original sensor resolution (set using :func:`setResolution`)

  .. function:: setSensorCrop(x: float, y: float)

    Sets values in range :code:`[0, 1]` as the cropping parameters, determining the size of the cropped box

  .. function:: getSensorCrop() -> Tuple[float, float]

    Returns the x and y parameters of the sensor crop set previously using :func:`setSensorCrop`

  .. function:: getSensorCropX() -> float

    Returns the x parameter of the sensor crop set previously using :func:`setSensorCrop`

  .. function:: getSensorCropY() -> float

    Returns the y parameter of the sensor crop set previously using :func:`setSensorCrop`

  .. function:: setWaitForConfigInput(wait: bool)

    If set to :code:`True`, frames from the camera sensor will only be processed and sent to outputs when the config
    information arrives

  .. function:: getWaitForConfigInput() -> bool

    Returns the value previously set using :func:`setWaitForConfigInput`

  .. function:: setPreviewKeepAspectRatio(keep: bool)

    If set to :code:`True`, the :attr:`preview` output will be cropped and resized to retain the h/w proportion of the
    camera resolution. Otherwise, the image will be squished in either direction to achieve exact output specified using
    :func:`setPreviewSize`

  .. function:: getPreviewKeepAspectRatio() -> bool

    Returns the value previously set using :func:`setPreviewKeepAspectRatio`


.. class:: MonoCamera
  :canonical: depthai.MonoCamera

  Represents an XLink stream of data from host into device

  **Outputs**

  .. attribute:: out

    Mono camera video stream, sending grayscale frames

  **Methods**

  .. function:: setBoardSocket()

    Assigns the camera socket to the node

  .. function:: getBoardSocket()

    Returns the assigned board socket

  .. function:: setResolution(resolution: MonoCameraProperties.SensorResolution)

    Sets the camera sensor resolution, determining the maximum resolution that can be obtained from this node

  .. function:: getResolution() -> MonoCameraProperties.SensorResolution

    Returns camera resolution previously set using :func:`setResolution`

  .. function:: setFps(fps: float)

    Limits the FPS of the node, allowing e.g. to decrease the amount of frames being produced by this node

  .. function:: getFps() -> float

    Returns the current FPS limit

  .. function:: getResolutionSize() -> Tuple[int, int]

    Returns the sensor resolution dimensions

  .. function:: getResolutionWidth() -> int

    Returns the sensor resolution width

  .. function:: getResolutionHeight() -> int

    Returns the sensor resolution height


.. class:: NeuralNetwork
  :canonical: depthai.NeuralNetwork

  Represents an XLink stream of data from host into device

  **Inputs**

  .. attribute:: input

    Neural network input, on which the inference will be ran

  **Outputs**

  .. attribute:: out

    Inference results output, all neural network outputs will be send through this output

  .. function:: setBlobPath(path: str)

    Sets the neural network blob path, being the actual neural network to be ran

  .. function:: setNumPoolFrames(numFrames: int)

    Specifies how many nn results will the node keep buffered if not received by a consumer. Upon reaching the limit,
    the node stops and waits for the results to be consumed before producing new ones


.. class:: ImageManip
  :canonical: depthai.ImageManip

  Represents an XLink stream of data from host into device

  **Inputs**

  .. attribute:: inputConfig

    Linkable to :class:`ImageManipConfig`, allowing to modify crop area, horizontal flip, frame datatype etc.

  .. attribute:: inputImage

    Receives the frames that should be manipulated in this node

  **Outputs**

  .. attribute:: out

    Result frame, after manipulation

  **Methods**

  .. function:: setCropRect(xmin: float, ymin: float, xmax: float, ymax: float)

    Allows to crop only the desired section of the image

  .. function:: setCenterCrop(ratio: float, whRatio: float)

    Allows to specify arbitrary crop to the image.

    :code:`whRatio` determines width/height ratio of the cropped section (white box in the image below, :code:`whRatio` is set to :code:`1`),

    :code:`ratio` is determining the actual size of the cropped section (green box in the image below, :code:`ratio` is set to :code:`0.7`)

    .. image:: /_static/images/references/centerCrop.png
      :alt: 1097 top

  .. function:: setResize(w: int, h: int)

      Resizes the frame to specified width and height

  .. function:: setResizeThumbnail(w: int, h: int, bgRed: int, bgGreen: int, bgBlue: int)

      Resizes the frame, preserving the original aspect ratio, filling in the missing space with specified color

  .. function:: setFrameType(type: RawImgFrame.Type)

      Modifies the input frame to be in the specified image frame type (one of :class:`RawImgFrame.Type`)

  .. function:: setHorizontalFlip(flip: bool)

      If set to :code:`True`, flips the received frame horizontally

  .. function:: setKeepAspectRatio(keep: bool)

      If set to :code:`True`, the output will be cropped and resized to retain the h/w proportion of the
      input resolution. Otherwise, the image will be squished in either direction to achieve exact output specified

  .. function:: setWaitForConfigInput(wait: bool)

    If set to :code:`True`, frames will only be processed when the config information arrives

  .. function:: setNumFramesPool()

    Specifies how many results will the node keep buffered if not received by a consumer. Upon reaching the limit,
    the node stops and waits for the results to be consumed before producing new ones

  .. function:: setMaxOutputFrameSize(maxFrameSize: int)

    Limits the maximum frame size that is allowed to be send as an output of the node


.. class:: StereoDepth
  :canonical: depthai.StereoDepth

  Represents an XLink stream of data from host into device

  **Inputs**

  .. attribute:: left

    Input for frames from left grayscale camera

  .. attribute:: right

    Input for frames from right grayscale camera

  **Outputs**

  .. attribute:: depth

    Outputs a raw depth frame, enabled by calling :func:`setOutputDepth` with :code:`True`. Cannot be used together with :attr:`disparity: output

  .. attribute:: disparity

    Outputs a disparity matrix. Cannot be used together with :attr:`depth`

  .. attribute:: syncedLeft

    Outputs left frame used in depth calculations

  .. attribute:: syncedRight

    Outputs right frame used in depth calculations

  .. attribute:: rectifiedLeft

    Outputs left rectified frame, see `more info about rectification <https://en.wikipedia.org/wiki/Image_rectification>`__

  .. attribute:: rectifiedRight

    Outputs right rectified frame, see `more info about rectification <https://en.wikipedia.org/wiki/Image_rectification>`__

  **Methods**

  .. function:: loadCalibrationFile(path: str)

    Specifies a calibration file path to be loaded for depth calculations. Uses :func:`loadCalibrationData` internally

  .. function:: loadCalibrationData(data: List[int])

    Specifies a calibration data to be loaded for depth calculations

  .. function:: setEmptyCalibration()

    Replaces any loaded calibration data with an empty array

  .. function:: setInputResolution(width: int, height: int)

    Specifies input size of the :code:`left` / :code:`right` inputs. Most of the time, calling this function is not needed,
    useful when input frames don't come from mono cameras but directly from host

  .. function:: setMedianFilter(median: StereoDepthProperties.MedianFilter)

    Specifies which median filter should be used during depth calculations. May be one of the :class:`StereoDepthProperties.MedianFilter`

  .. function:: setConfidenceThreshold(confThr: int)

    Sets the confidence threshold of the depth calculating algorithm, specifying when a point on the depth projection will
    be considered a valid or not

  .. function:: setLeftRightCheck(enable: bool)

    Enables Left/Right check during depth calculations

  .. function:: setSubpixel(enable: bool)

    Enables subpixel filtering during depth calculations

  .. function:: setExtendedDisparity(enable: bool)

    Enables extended disparity during depth calculations

  .. function:: setRectifyEdgeFillColor(color: int)

    Sets the color of the rectification edge (cropped part during `rectification <https://en.wikipedia.org/wiki/Image_rectification>`__)

  .. function:: setRectifyMirrorFrame(enable: bool)

    Enables mirroring of the rectified frames

  .. function:: setOutputRectified(enable: bool)

    Enables :attr:`rectifiedLeft` and :attr:`rectifiedRight` outputs

  .. function:: setOutputDepth(enable: bool)

    If set to :code:`True`, the :attr:`depth` output will be produced, otherwise :attr:`disparity` will be active


.. class:: VideoEncoder
  :canonical: depthai.VideoEncoder

  **Inputs**

  .. attribute:: input

  **Outputs**

  .. attribute:: bitstream

  **Methods**

  .. function:: setDefaultProfilePreset()

  .. function:: setNumFramesPool()

  .. function:: getNumFramesPool()

  .. function:: setRateControlMode()

  .. function:: getRateControlMode()

  .. function:: setProfile()

  .. function:: getProfile()

  .. function:: setBitrate()

  .. function:: getBitrate()

  .. function:: setKeyframeFrequency()

  .. function:: getKeyframeFrequency()

  .. function:: setNumBFrames()

  .. function:: getNumBFrames()

  .. function:: setQuality()

  .. function:: getQuality()

  .. function:: getWidth()

  .. function:: getHeight()

  .. function:: getSize() -> Tuple[int, int]

  .. function:: setFrameRate()

  .. function:: getFrameRate()


.. class:: CameraBoardSocket
  :canonical: depthai.CameraBoardSocket

  **Outputs**

  .. attribute:: AUTO

  .. attribute:: RGB

  .. attribute:: LEFT

  .. attribute:: RIGHT


.. class:: ColorCameraProperties
  :canonical: depthai.ColorCameraProperties

  **Outputs**

  .. attribute:: boardSocket

  .. attribute:: colorOrder

  .. attribute:: interleaved

  .. attribute:: previewHeight

  .. attribute:: previewWidth

  .. attribute:: resolution

  .. attribute:: fps

  .. attribute:: videoHeight

  .. attribute:: videoWidth

  .. attribute:: stillHeight

  .. attribute:: stillWidth

  .. attribute:: sensorCropX

  .. attribute:: sensorCropY


.. class:: ColorCameraProperties.SensorResolution
  :canonical: depthai.ColorCameraProperties.SensorResolution

  **Outputs**

  .. attribute:: THE_1080_P

  .. attribute:: THE_4_K

  .. attribute:: THE_12_MP


.. class:: ColorCameraProperties.ColorOrder
  :canonical: depthai.ColorCameraProperties.ColorOrder

  **Outputs**

  .. attribute:: BGR

  .. attribute:: RGB


.. class:: MonoCameraProperties
  :canonical: depthai.MonoCameraProperties

  **Outputs**

  .. attribute:: boardSocket

  .. attribute:: resolution

  .. attribute:: fps


.. class:: MonoCameraProperties.SensorResolution
  :canonical: depthai.MonoCameraProperties.SensorResolution

  **Outputs**

  .. attribute:: THE_720_P

  .. attribute:: THE_800_P

  .. attribute:: THE_400_P


.. class:: StereoDepthProperties
  :canonical: depthai.StereoDepthProperties

  **Outputs**

  .. attribute:: calibration

  .. attribute:: median

  .. attribute:: confidenceThreshold

  .. attribute:: enableLeftRightCheck

  .. attribute:: enableSubpixel

  .. attribute:: enableExtendedDisparity

  .. attribute:: rectifyMirrorFrame

  .. attribute:: rectifyEdgeFillColor

  .. attribute:: enableOutputRectified

  .. attribute:: enableOutputDepth

  .. attribute:: width

  .. attribute:: height


.. class:: StereoDepthProperties.MedianFilter
  :canonical: depthai.StereoDepthProperties.MedianFilter

  **Outputs**

  .. attribute:: MEDIAN_OFF

  .. attribute:: KERNEL_3x3

  .. attribute:: KERNEL_5x5

  .. attribute:: KERNEL_7x7


.. class:: VideoEncoderProperties
  :canonical: depthai.VideoEncoderProperties

  **Outputs**

  .. attribute:: bitrate

  .. attribute:: keyframeFrequency

  .. attribute:: maxBitrate

  .. attribute:: numBFrames

  .. attribute:: numFramesPool

  .. attribute:: profile

  .. attribute:: quality

  .. attribute:: rateCtrlMode

  .. attribute:: width

  .. attribute:: height


.. class:: VideoEncoderProperties.Profile
  :canonical: depthai.VideoEncoderProperties.Profile

  **Outputs**

  .. attribute:: H264_BASELINE

  .. attribute:: H264_HIGH

  .. attribute:: H264_MAIN

  .. attribute:: H265_MAIN

  .. attribute:: MJPEG


.. class:: VideoEncoderProperties.RateControlMode
  :canonical: depthai.VideoEncoderProperties.RateControlMode

  **Outputs**

  .. attribute:: CBR

  .. attribute:: VBR


.. class:: SPIOut
  :canonical: depthai.SPIOut

  **Outputs**

  .. attribute:: input

  .. function:: setStreamName()

  .. function:: setBusId()



.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Contents:

   depthai.XLinkIn <?dummy=http://#XLinkIn>
   depthai.XLinkOut <?dummy=http://#XLinkOut>
   depthai.ColorCamera <?dummy=http://#ColorCamera>
   depthai.MonoCamera <?dummy=http://#MonoCamera>
   depthai.NeuralNetwork <?dummy=http://#NeuralNetwork>
   depthai.ImageManip <?dummy=http://#ImageManip>
   depthai.StereoDepth <?dummy=http://#StereoDepth>
