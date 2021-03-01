#include "NodeBindings.hpp"

#include "depthai/pipeline/Node.hpp"
#include "depthai/pipeline/node/XLinkIn.hpp"
#include "depthai/pipeline/node/XLinkOut.hpp"
#include "depthai/pipeline/node/ColorCamera.hpp"
#include "depthai/pipeline/node/MonoCamera.hpp"
#include "depthai/pipeline/node/StereoDepth.hpp"
#include "depthai/pipeline/node/NeuralNetwork.hpp"
#include "depthai/pipeline/node/VideoEncoder.hpp"
#include "depthai/pipeline/node/ImageManip.hpp"
#include "depthai/pipeline/node/SPIOut.hpp"
#include "depthai/pipeline/node/DetectionNetwork.hpp"
#include "depthai/pipeline/node/SystemLogger.hpp"

// Libraries
#include "hedley/hedley.h"

void NodeBindings::bind(pybind11::module& m){

    using namespace dai;
    using namespace dai::node;


    // Base 'Node' class binding
    py::class_<Node, std::shared_ptr<Node>> pyNode(m, "Node", DOC(dai, Node));
    pyNode 
        .def_readonly("id", &Node::id, DOC(dai, Node, id))
        .def("getName", &Node::getName, DOC(dai, Node, getName))
        .def("getOutputs", &Node::getOutputs, DOC(dai, Node, getOutputs))
        .def("getInputs", &Node::getInputs, DOC(dai, Node, getInputs))
        .def("getAssets", &Node::getAssets, DOC(dai, Node, getAssets))
    ;

    // Node::Input bindings
    py::class_<Node::Input>(pyNode, "Input")
        .def("setBlocking", &Node::Input::setBlocking, py::arg("blocking"), DOC(dai, Node, Input, setBlocking))
        .def("getBlocking", &Node::Input::getBlocking, DOC(dai, Node, Input, getBlocking))
        .def("setQueueSize", &Node::Input::setQueueSize, py::arg("size"), DOC(dai, Node, Input, setQueueSize))
        .def("getQueueSize", &Node::Input::getQueueSize, DOC(dai, Node, Input, getQueueSize))
    ;
    // Node::Output bindings
    py::class_<Node::Output>(pyNode, "Output")
        .def("canConnect", &Node::Output::canConnect, py::arg("in"), DOC(dai, Node, Output, canConnect))
        .def("link", &Node::Output::link, py::arg("in"), DOC(dai, Node, Output, link))
        .def("unlink", &Node::Output::unlink, py::arg("in"), DOC(dai, Node, Output, unlink))
        .def("getConnections", &Node::Output::getConnections, DOC(dai, Node, Output, getConnections))
    ;
    // Node::Id bindings
    py::class_<Node::Id>(pyNode, "Id", "Node identificator. Unique for every node on a single Pipeline");

    // Node::Connection bindings
    py::class_<Node::Connection>(pyNode, "Connection", DOC(dai, Node, Connection))
        .def_property("outputId", [](Node::Connection& conn) { return conn.outputId; }, [](Node::Connection& conn, Node::Id id) {conn.outputId = id; }, DOC(dai, Node, Connection, outputId))
        .def_property("outputName", [](Node::Connection& conn) { return conn.outputName; }, [](Node::Connection& conn, std::string name) {conn.outputName = name; }, DOC(dai, Node, Connection, outputName))
        .def_property("inputId", [](Node::Connection& conn) { return conn.inputId; }, [](Node::Connection& conn, Node::Id id) {conn.inputId = id; }, DOC(dai, Node, Connection, inputId))
        .def_property("inputName", [](Node::Connection& conn) { return conn.inputName; }, [](Node::Connection& conn, std::string name) {conn.inputName = name; }, DOC(dai, Node, Connection, inputName))
    ;
    // MSVC errors out with: 
    // Error C2326 'void NodeBindings::bind(pybind11::module &)': function cannot access 'dai::Node::Connection::outputId'
    // ...
    // py::class_<Node::Connection>(pyNode, "Connection")
    //     .def_readwrite("outputId", &dai::Node::Connection::outputId)
    //     .def_readwrite("outputName", &dai::Node::Connection::outputName)
    //     .def_readwrite("inputId", &dai::Node::Connection::inputId)
    //     .def_readwrite("inputName", &dai::Node::Connection::inputName)
    // ;

    //// Bindings for actual nodes

    // XLinkIn node
    py::class_<XLinkIn, Node, std::shared_ptr<XLinkIn>>(m, "XLinkIn", DOC(dai, node, XLinkIn))
        .def_readonly("out", &XLinkIn::out, DOC(dai, node, XLinkIn, out))
        .def("setStreamName", &XLinkIn::setStreamName, py::arg("streamName"), DOC(dai, node, XLinkIn, setStreamName))
        .def("setMaxDataSize", &XLinkIn::setMaxDataSize, py::arg("maxDataSize"), DOC(dai, node, XLinkIn, setMaxDataSize))
        .def("setNumFrames",  &XLinkIn::setNumFrames, py::arg("numFrames"), DOC(dai, node, XLinkIn, setNumFrames)) 
        .def("getStreamName", &XLinkIn::getStreamName, DOC(dai, node, XLinkIn, getStreamName))
        .def("getMaxDataSize", &XLinkIn::getMaxDataSize, DOC(dai, node, XLinkIn, getMaxDataSize))
        .def("getNumFrames",  &XLinkIn::getNumFrames, DOC(dai, node, XLinkIn, getNumFrames))     
        ;

    // XLinkOut node
    py::class_<XLinkOut, Node, std::shared_ptr<XLinkOut>>(m, "XLinkOut", DOC(dai, node, XLinkOut))
        .def_readonly("input", &XLinkOut::input, DOC(dai, node, XLinkOut, input))
        .def("setStreamName", &XLinkOut::setStreamName, py::arg("streamName"), DOC(dai, node, XLinkOut, setStreamName))
        .def("setFpsLimit", &XLinkOut::setFpsLimit, py::arg("fpsLimit"), DOC(dai, node, XLinkOut, setFpsLimit))
        .def("getStreamName", &XLinkOut::getStreamName, DOC(dai, node, XLinkOut, getStreamName))
        .def("getFpsLimit", &XLinkOut::getFpsLimit, DOC(dai, node, XLinkOut, getFpsLimit))
        .def("setMetadataOnly", &XLinkOut::setMetadataOnly, DOC(dai, node, XLinkOut, setMetadataOnly))
        .def("getMetadataOnly", &XLinkOut::getMetadataOnly, DOC(dai, node, XLinkOut, getMetadataOnly))
        ;

    // ColorCamera node
    py::class_<ColorCamera, Node, std::shared_ptr<ColorCamera>>(m, "ColorCamera", DOC(dai, node, ColorCamera))
        .def_readonly("inputConfig", &ColorCamera::inputConfig, DOC(dai, node, ColorCamera, inputConfig))
        .def_readonly("inputControl", &ColorCamera::inputControl, DOC(dai, node, ColorCamera, inputControl))
        .def_readonly("initialControl", &ColorCamera::initialControl, DOC(dai, node, ColorCamera, initialControl))
        .def_readonly("video", &ColorCamera::video, DOC(dai, node, ColorCamera, video))
        .def_readonly("preview", &ColorCamera::preview, DOC(dai, node, ColorCamera, preview))
        .def_readonly("still", &ColorCamera::still, DOC(dai, node, ColorCamera, still))
        .def("setCamId", [](ColorCamera& c, int64_t id) {
            // Issue an deprecation warning
            PyErr_WarnEx(PyExc_DeprecationWarning, "setCamId() is deprecated, use setBoardSocket() instead.", 1);
            HEDLEY_DIAGNOSTIC_PUSH
            HEDLEY_DIAGNOSTIC_DISABLE_DEPRECATED
            c.setCamId(id);
            HEDLEY_DIAGNOSTIC_POP
        })
        .def("getCamId", [](ColorCamera& c) {
            // Issue an deprecation warning
            PyErr_WarnEx(PyExc_DeprecationWarning, "getCamId() is deprecated, use getBoardSocket() instead.", 1);
            HEDLEY_DIAGNOSTIC_PUSH
            HEDLEY_DIAGNOSTIC_DISABLE_DEPRECATED
            return c.getCamId();            
            HEDLEY_DIAGNOSTIC_POP
        })
        .def("setBoardSocket", &ColorCamera::setBoardSocket, py::arg("boardSocket"), DOC(dai, node, ColorCamera, setBoardSocket))
        .def("getBoardSocket", &ColorCamera::getBoardSocket, DOC(dai, node, ColorCamera, getBoardSocket))
        .def("setImageOrientation", &ColorCamera::setImageOrientation, py::arg("boardSocket"), DOC(dai, node, ColorCamera, setImageOrientation))
        .def("getImageOrientation", &ColorCamera::getImageOrientation, DOC(dai, node, ColorCamera, getImageOrientation))
        .def("setColorOrder", &ColorCamera::setColorOrder, py::arg("colorOrder"), DOC(dai, node, ColorCamera, setColorOrder))
        .def("getColorOrder", &ColorCamera::getColorOrder, DOC(dai, node, ColorCamera, getColorOrder))
        .def("setInterleaved", &ColorCamera::setInterleaved, py::arg("interleaved"), DOC(dai, node, ColorCamera, setInterleaved))
        .def("getInterleaved", &ColorCamera::getInterleaved, DOC(dai, node, ColorCamera, getInterleaved))
        .def("setFp16", &ColorCamera::setFp16, py::arg("fp16"), DOC(dai, node, ColorCamera, setFp16))
        .def("getFp16", &ColorCamera::getFp16, DOC(dai, node, ColorCamera, getFp16))
        .def("setPreviewSize", &ColorCamera::setPreviewSize, py::arg("width"), py::arg("height"), DOC(dai, node, ColorCamera, setPreviewSize))
        .def("setVideoSize", &ColorCamera::setVideoSize, py::arg("width"), py::arg("height"), DOC(dai, node, ColorCamera, setVideoSize))
        .def("setStillSize", &ColorCamera::setStillSize, py::arg("width"), py::arg("height"), DOC(dai, node, ColorCamera, setStillSize))
        .def("setResolution", &ColorCamera::setResolution, py::arg("resolution"), DOC(dai, node, ColorCamera, setResolution))
        .def("getResolution", &ColorCamera::getResolution, DOC(dai, node, ColorCamera, getResolution))
        .def("setFps", &ColorCamera::setFps, py::arg("fps"), DOC(dai, node, ColorCamera, setFps))
        .def("getFps", &ColorCamera::getFps, DOC(dai, node, ColorCamera, getFps))
        .def("getPreviewSize", &ColorCamera::getPreviewSize, DOC(dai, node, ColorCamera, getPreviewSize))
        .def("getPreviewWidth", &ColorCamera::getPreviewWidth, DOC(dai, node, ColorCamera, getPreviewWidth))
        .def("getPreviewHeight", &ColorCamera::getPreviewHeight, DOC(dai, node, ColorCamera, getPreviewHeight))
        .def("getVideoSize", &ColorCamera::getVideoSize, DOC(dai, node, ColorCamera, getVideoSize))
        .def("getVideoWidth", &ColorCamera::getVideoWidth, DOC(dai, node, ColorCamera, getVideoWidth))
        .def("getVideoHeight", &ColorCamera::getVideoHeight, DOC(dai, node, ColorCamera, getVideoHeight))
        .def("getStillSize", &ColorCamera::getStillSize, DOC(dai, node, ColorCamera, getStillSize))
        .def("getStillWidth", &ColorCamera::getStillWidth, DOC(dai, node, ColorCamera, getStillWidth))
        .def("getStillHeight", &ColorCamera::getStillHeight, DOC(dai, node, ColorCamera, getStillHeight))
        .def("getResolutionSize", &ColorCamera::getResolutionSize, DOC(dai, node, ColorCamera, getResolutionSize))
        .def("getResolutionWidth", &ColorCamera::getResolutionWidth, DOC(dai, node, ColorCamera, getResolutionWidth))
        .def("getResolutionHeight", &ColorCamera::getResolutionHeight, DOC(dai, node, ColorCamera, getResolutionHeight))
        .def("sensorCenterCrop", &ColorCamera::sensorCenterCrop, DOC(dai, node, ColorCamera, sensorCenterCrop))
        .def("setSensorCrop", &ColorCamera::setSensorCrop, py::arg("x"), py::arg("y"), DOC(dai, node, ColorCamera, setSensorCrop))
        .def("getSensorCrop", &ColorCamera::getSensorCrop, DOC(dai, node, ColorCamera, getSensorCrop))
        .def("getSensorCropX", &ColorCamera::getSensorCropX, DOC(dai, node, ColorCamera, getSensorCropX))
        .def("getSensorCropY", &ColorCamera::getSensorCropY, DOC(dai, node, ColorCamera, getSensorCropY))
        .def("setWaitForConfigInput", &ColorCamera::setWaitForConfigInput, py::arg("wait"), DOC(dai, node, ColorCamera, setWaitForConfigInput))
        .def("getWaitForConfigInput", &ColorCamera::getWaitForConfigInput, DOC(dai, node, ColorCamera, getWaitForConfigInput))
        .def("setPreviewKeepAspectRatio", &ColorCamera::setPreviewKeepAspectRatio, py::arg("keep"), DOC(dai, node, ColorCamera, setPreviewKeepAspectRatio))
        .def("getPreviewKeepAspectRatio", &ColorCamera::getPreviewKeepAspectRatio, DOC(dai, node, ColorCamera, getPreviewKeepAspectRatio))
        ;
    


    // NeuralNetwork node
    py::class_<NeuralNetwork, Node, std::shared_ptr<NeuralNetwork>>(m, "NeuralNetwork", DOC(dai, node, NeuralNetwork))
        .def_readonly("input", &NeuralNetwork::input, DOC(dai, node, NeuralNetwork, input))
        .def_readonly("out", &NeuralNetwork::out, DOC(dai, node, NeuralNetwork, out))
        .def_readonly("passthrough", &NeuralNetwork::passthrough, DOC(dai, node, NeuralNetwork, passthrough))
        .def("setBlobPath", &NeuralNetwork::setBlobPath, py::arg("path"), DOC(dai, node, NeuralNetwork, setBlobPath))
        .def("setNumPoolFrames", &NeuralNetwork::setNumPoolFrames, py::arg("numFrames"), DOC(dai, node, NeuralNetwork, setNumPoolFrames))
        .def("setNumInferenceThreads", &NeuralNetwork::setNumInferenceThreads, py::arg("numThreads"), DOC(dai, node, NeuralNetwork, setNumInferenceThreads))
        .def("setNumNCEPerInferenceThread", &NeuralNetwork::setNumNCEPerInferenceThread, py::arg("numNCEPerThread"), DOC(dai, node, NeuralNetwork, setNumNCEPerInferenceThread))
        .def("getNumInferenceThreads", &NeuralNetwork::getNumInferenceThreads, DOC(dai, node, NeuralNetwork, getNumInferenceThreads))
        ;


    // ImageManip node
    py::class_<ImageManip, Node, std::shared_ptr<ImageManip>>(m, "ImageManip", DOC(dai, node, ImageManip))
        .def_readonly("inputConfig", &ImageManip::inputConfig, DOC(dai, node, ImageManip, inputConfig))
        .def_readonly("inputImage", &ImageManip::inputImage, DOC(dai, node, ImageManip, inputImage))
        .def_readonly("out", &ImageManip::out, DOC(dai, node, ImageManip, out))
        .def_readonly("initialConfig", &ImageManip::initialConfig, DOC(dai, node, ImageManip, initialConfig))
        // setters
        
        .def("setCropRect", [](ImageManip& im, float xmin, float ymin, float xmax, float ymax) {
            // Issue a deprecation warning
            PyErr_WarnEx(PyExc_DeprecationWarning, "setCropRect() is deprecated, use initialConfig.setCropRect() instead.", 1);
            HEDLEY_DIAGNOSTIC_PUSH
            HEDLEY_DIAGNOSTIC_DISABLE_DEPRECATED
            im.setCropRect(xmin, ymin, xmax, ymax);
            HEDLEY_DIAGNOSTIC_POP
        })
        .def("setCenterCrop", [](ImageManip& im, float ratio, float whRatio = 1.0f) {
            // Issue a deprecation warning
            PyErr_WarnEx(PyExc_DeprecationWarning, "setCenterCrop() is deprecated, use initialConfig.setCenterCrop() instead.", 1);
            HEDLEY_DIAGNOSTIC_PUSH
            HEDLEY_DIAGNOSTIC_DISABLE_DEPRECATED
            im.setCenterCrop(ratio, whRatio);
            HEDLEY_DIAGNOSTIC_POP
        })

        .def("setResize", [](ImageManip& im, int w, int h) {
            // Issue a deprecation warning
            PyErr_WarnEx(PyExc_DeprecationWarning, "setResize() is deprecated, use initialConfig.setResize() instead.", 1);
            HEDLEY_DIAGNOSTIC_PUSH
            HEDLEY_DIAGNOSTIC_DISABLE_DEPRECATED
            im.setResize(w, h);
            HEDLEY_DIAGNOSTIC_POP
        })

        .def("setResizeThumbnail", [](ImageManip& im, int w, int h, int bgRed = 0, int bgGreen = 0, int bgBlue = 0) {
            // Issue a deprecation warning
            PyErr_WarnEx(PyExc_DeprecationWarning, "setResizeThumbnail() is deprecated, use initialConfig.setResizeThumbnail() instead.", 1);
            HEDLEY_DIAGNOSTIC_PUSH
            HEDLEY_DIAGNOSTIC_DISABLE_DEPRECATED
            im.setResizeThumbnail(w, h, bgRed, bgGreen, bgBlue);
            HEDLEY_DIAGNOSTIC_POP
        })

        .def("setFrameType", [](ImageManip& im, dai::RawImgFrame::Type name) {
            // Issue a deprecation warning
            PyErr_WarnEx(PyExc_DeprecationWarning, "setFrameType() is deprecated, use initialConfig.setFrameType() instead.", 1);
            HEDLEY_DIAGNOSTIC_PUSH
            HEDLEY_DIAGNOSTIC_DISABLE_DEPRECATED
            im.setFrameType(name);
            HEDLEY_DIAGNOSTIC_POP
        })

        .def("setHorizontalFlip", [](ImageManip& im, bool flip) {
            // Issue a deprecation warning
            PyErr_WarnEx(PyExc_DeprecationWarning, "setHorizontalFlip() is deprecated, use initialConfig.setHorizontalFlip() instead.", 1);
            HEDLEY_DIAGNOSTIC_PUSH
            HEDLEY_DIAGNOSTIC_DISABLE_DEPRECATED
            im.setHorizontalFlip(flip);
            HEDLEY_DIAGNOSTIC_POP
        })
        
        .def("setKeepAspectRatio", &ImageManip::setKeepAspectRatio, DOC(dai, node, ImageManip, setKeepAspectRatio))

        .def("setWaitForConfigInput", &ImageManip::setWaitForConfigInput, DOC(dai, node, ImageManip, setWaitForConfigInput))
        .def("setNumFramesPool", &ImageManip::setNumFramesPool, DOC(dai, node, ImageManip, setNumFramesPool))
        .def("setMaxOutputFrameSize", &ImageManip::setMaxOutputFrameSize, DOC(dai, node, ImageManip, setMaxOutputFrameSize))
        ;

     // MonoCamera node
    py::class_<MonoCamera, Node, std::shared_ptr<MonoCamera>>(m, "MonoCamera", DOC(dai, node, MonoCamera))
        .def_readonly("inputControl", &MonoCamera::inputControl, DOC(dai, node, MonoCamera, inputControl))
        .def_readonly("out",  &MonoCamera::out, DOC(dai, node, MonoCamera, out))
        .def_readonly("initialControl",  &MonoCamera::initialControl, DOC(dai, node, MonoCamera, initialControl))
        .def("setCamId", [](MonoCamera& c, int64_t id) {
            // Issue an deprecation warning
            PyErr_WarnEx(PyExc_DeprecationWarning, "setCamId() is deprecated, use setBoardSocket() instead.", 1);
            HEDLEY_DIAGNOSTIC_PUSH
            HEDLEY_DIAGNOSTIC_DISABLE_DEPRECATED
            c.setCamId(id);
            HEDLEY_DIAGNOSTIC_POP
        })
        .def("getCamId", [](MonoCamera& c) {
            // Issue an deprecation warning
            PyErr_WarnEx(PyExc_DeprecationWarning, "getCamId() is deprecated, use getBoardSocket() instead.", 1);
            HEDLEY_DIAGNOSTIC_PUSH
            HEDLEY_DIAGNOSTIC_DISABLE_DEPRECATED
            return c.getCamId();
            HEDLEY_DIAGNOSTIC_POP
        })
        .def("setBoardSocket", &MonoCamera::setBoardSocket, py::arg("boardSocket"), DOC(dai, node, MonoCamera, setBoardSocket))
        .def("getBoardSocket", &MonoCamera::getBoardSocket, DOC(dai, node, MonoCamera, getBoardSocket))
        .def("setImageOrientation", &MonoCamera::setImageOrientation, py::arg("imageOrientation"), DOC(dai, node, MonoCamera, setImageOrientation))
        .def("getImageOrientation", &MonoCamera::getImageOrientation, DOC(dai, node, MonoCamera, getImageOrientation))
        .def("setResolution", &MonoCamera::setResolution, py::arg("resolution"), DOC(dai, node, MonoCamera, setResolution))
        .def("getResolution", &MonoCamera::getResolution, DOC(dai, node, MonoCamera, getResolution))
        .def("setFps",        &MonoCamera::setFps, py::arg("fps"), DOC(dai, node, MonoCamera, setFps))
        .def("getFps",        &MonoCamera::getFps, DOC(dai, node, MonoCamera, getFps))
        .def("getResolutionSize", &MonoCamera::getResolutionSize, DOC(dai, node, MonoCamera, getResolutionSize))
        .def("getResolutionWidth", &MonoCamera::getResolutionWidth, DOC(dai, node, MonoCamera, getResolutionWidth))
        .def("getResolutionHeight", &MonoCamera::getResolutionHeight, DOC(dai, node, MonoCamera, getResolutionHeight))
        ;
        


    // StereoDepth node
    py::class_<StereoDepth, Node, std::shared_ptr<StereoDepth>>(m, "StereoDepth", DOC(dai, node, StereoDepth))
        .def_readonly("left",           &StereoDepth::left, DOC(dai, node, StereoDepth, left))
        .def_readonly("right",          &StereoDepth::right, DOC(dai, node, StereoDepth, right))
        .def_readonly("depth",          &StereoDepth::depth, DOC(dai, node, StereoDepth, depth))
        .def_readonly("disparity",      &StereoDepth::disparity, DOC(dai, node, StereoDepth, disparity))
        .def_readonly("syncedLeft",     &StereoDepth::syncedLeft, DOC(dai, node, StereoDepth, syncedLeft))
        .def_readonly("syncedRight",    &StereoDepth::syncedRight, DOC(dai, node, StereoDepth, syncedRight))
        .def_readonly("rectifiedLeft",  &StereoDepth::rectifiedLeft, DOC(dai, node, StereoDepth, rectifiedLeft))
        .def_readonly("rectifiedRight", &StereoDepth::rectifiedRight, DOC(dai, node, StereoDepth, rectifiedRight))
        .def("loadCalibrationFile",     &StereoDepth::loadCalibrationFile, py::arg("path"), DOC(dai, node, StereoDepth, loadCalibrationFile))
        .def("loadCalibrationData",     &StereoDepth::loadCalibrationData, py::arg("data"), DOC(dai, node, StereoDepth, loadCalibrationData))
        .def("setEmptyCalibration",     &StereoDepth::setEmptyCalibration, DOC(dai, node, StereoDepth, setEmptyCalibration))
        .def("setInputResolution",      &StereoDepth::setInputResolution, py::arg("width"), py::arg("height"), DOC(dai, node, StereoDepth, setInputResolution))
        .def("setMedianFilter",         &StereoDepth::setMedianFilter, py::arg("median"), DOC(dai, node, StereoDepth, setMedianFilter))
        .def("setConfidenceThreshold",  &StereoDepth::setConfidenceThreshold, py::arg("confThr"), DOC(dai, node, StereoDepth, setConfidenceThreshold))
        .def("setLeftRightCheck",       &StereoDepth::setLeftRightCheck, py::arg("enable"), DOC(dai, node, StereoDepth, setLeftRightCheck))
        .def("setSubpixel",             &StereoDepth::setSubpixel, py::arg("enable"), DOC(dai, node, StereoDepth, setSubpixel))
        .def("setExtendedDisparity",    &StereoDepth::setExtendedDisparity, py::arg("enable"), DOC(dai, node, StereoDepth, setExtendedDisparity))
        .def("setRectifyEdgeFillColor", &StereoDepth::setRectifyEdgeFillColor, py::arg("color"), DOC(dai, node, StereoDepth, setRectifyEdgeFillColor))
        .def("setRectifyMirrorFrame",   &StereoDepth::setRectifyMirrorFrame, py::arg("enable"), DOC(dai, node, StereoDepth, setRectifyMirrorFrame))
        .def("setOutputRectified",      &StereoDepth::setOutputRectified, py::arg("enable"), DOC(dai, node, StereoDepth, setOutputRectified))
        .def("setOutputDepth",          &StereoDepth::setOutputDepth, py::arg("enable"), DOC(dai, node, StereoDepth, setOutputDepth))
        ;

    // VideoEncoder node
    py::class_<VideoEncoder, Node, std::shared_ptr<VideoEncoder>>(m, "VideoEncoder", DOC(dai, node, VideoEncoder))
        .def_readonly("input", &VideoEncoder::input, DOC(dai, node, VideoEncoder, input), DOC(dai, node, VideoEncoder, input))
        .def_readonly("bitstream", &VideoEncoder::bitstream, DOC(dai, node, VideoEncoder, bitstream), DOC(dai, node, VideoEncoder, bitstream))        
        .def("setDefaultProfilePreset", (void(VideoEncoder::*)(int, int, float, VideoEncoderProperties::Profile))&VideoEncoder::setDefaultProfilePreset, py::arg("width"), py::arg("height"), py::arg("fps"), py::arg("profile"), DOC(dai, node, VideoEncoder, setDefaultProfilePreset))
        .def("setDefaultProfilePreset", (void(VideoEncoder::*)(std::tuple<int,int>, float, VideoEncoderProperties::Profile))&VideoEncoder::setDefaultProfilePreset, py::arg("size"), py::arg("fps"), py::arg("profile"), DOC(dai, node, VideoEncoder, setDefaultProfilePreset, 2))
        .def("setNumFramesPool", &VideoEncoder::setNumFramesPool, py::arg("frames"), DOC(dai, node, VideoEncoder, setNumFramesPool))
        .def("getNumFramesPool", &VideoEncoder::getNumFramesPool, DOC(dai, node, VideoEncoder, getNumFramesPool))
        .def("setRateControlMode", &VideoEncoder::setRateControlMode, py::arg("mode"), DOC(dai, node, VideoEncoder, setRateControlMode))
        .def("setProfile", &VideoEncoder::setProfile, py::arg("width"), py::arg("height"), py::arg("profile"), DOC(dai, node, VideoEncoder, setProfile))
        .def("setBitrate", &VideoEncoder::setBitrate, py::arg("bitrateKbps"), DOC(dai, node, VideoEncoder, setBitrate))
        .def("setKeyframeFrequency", &VideoEncoder::setKeyframeFrequency, py::arg("freq"), DOC(dai, node, VideoEncoder, setKeyframeFrequency))
        //.def("setMaxBitrate", &VideoEncoder::setMaxBitrate)
        .def("setNumBFrames", &VideoEncoder::setNumBFrames, py::arg("numBFrames"), DOC(dai, node, VideoEncoder, setNumBFrames))
        .def("setQuality", &VideoEncoder::setQuality, py::arg("quality"), DOC(dai, node, VideoEncoder, setQuality))
        .def("setFrameRate", &VideoEncoder::setFrameRate, py::arg("frameRate"), DOC(dai, node, VideoEncoder, setFrameRate))
        .def("getRateControlMode", &VideoEncoder::getRateControlMode, DOC(dai, node, VideoEncoder, getRateControlMode))
        .def("getProfile", &VideoEncoder::getProfile, DOC(dai, node, VideoEncoder, getProfile))
        .def("getBitrate", &VideoEncoder::getBitrate, DOC(dai, node, VideoEncoder, getBitrate))
        .def("getKeyframeFrequency", &VideoEncoder::getKeyframeFrequency, DOC(dai, node, VideoEncoder, getKeyframeFrequency))
        //.def("getMaxBitrate", &VideoEncoder::getMaxBitrate)
        .def("getNumBFrames", &VideoEncoder::getNumBFrames, DOC(dai, node, VideoEncoder, getNumBFrames))
        .def("getQuality", &VideoEncoder::getQuality, DOC(dai, node, VideoEncoder, getQuality))
        .def("getWidth", &VideoEncoder::getWidth, DOC(dai, node, VideoEncoder, getWidth))
        .def("getHeight", &VideoEncoder::getHeight, DOC(dai, node, VideoEncoder, getHeight))
        .def("getFrameRate", &VideoEncoder::getFrameRate, DOC(dai, node, VideoEncoder, getFrameRate))
        .def("getSize", &VideoEncoder::getSize, DOC(dai, node, VideoEncoder, getSize))
    ;

    // SPIOut node
    py::class_<SPIOut, Node, std::shared_ptr<SPIOut>>(m, "SPIOut", DOC(dai, node, SPIOut))
        .def_readonly("input", &SPIOut::input, DOC(dai, node, SPIOut, input))
        .def("setStreamName", &SPIOut::setStreamName, py::arg("name"), DOC(dai, node, SPIOut, setStreamName))
        .def("setBusId", &SPIOut::setBusId, py::arg("id"), DOC(dai, node, SPIOut, setBusId))
        ;

    py::class_<DetectionNetwork, NeuralNetwork, std::shared_ptr<DetectionNetwork>>(m, "DetectionNetwork", DOC(dai, node, DetectionNetwork))
        .def_readonly("input", &DetectionNetwork::input, DOC(dai, node, DetectionNetwork, input))
        .def_readonly("out", &DetectionNetwork::out, DOC(dai, node, DetectionNetwork, out))
        .def_readonly("passthrough", &DetectionNetwork::passthrough, DOC(dai, node, DetectionNetwork, passthrough))
        .def("setConfidenceThreshold", &DetectionNetwork::setConfidenceThreshold, py::arg("thresh"), DOC(dai, node, DetectionNetwork, setConfidenceThreshold))
        ;

    // MobileNetDetectionNetwork node
    py::class_<MobileNetDetectionNetwork, DetectionNetwork, std::shared_ptr<MobileNetDetectionNetwork>>(m, "MobileNetDetectionNetwork", DOC(dai, node, MobileNetDetectionNetwork))
        ;

    // YoloDetectionNetwork node
    py::class_<YoloDetectionNetwork, DetectionNetwork, std::shared_ptr<YoloDetectionNetwork>>(m, "YoloDetectionNetwork", DOC(dai, node, YoloDetectionNetwork))
        .def("setNumClasses", &YoloDetectionNetwork::setNumClasses, py::arg("numClasses"), DOC(dai, node, YoloDetectionNetwork, setNumClasses))
        .def("setCoordinateSize", &YoloDetectionNetwork::setCoordinateSize, py::arg("coordinates"), DOC(dai, node, YoloDetectionNetwork, setCoordinateSize))
        .def("setAnchors", &YoloDetectionNetwork::setAnchors, py::arg("anchors"), DOC(dai, node, YoloDetectionNetwork, setAnchors))
        .def("setAnchorMasks", &YoloDetectionNetwork::setAnchorMasks, py::arg("anchorMasks"), DOC(dai, node, YoloDetectionNetwork, setAnchorMasks))
        .def("setIouThreshold", &YoloDetectionNetwork::setIouThreshold, py::arg("thresh"), DOC(dai, node, YoloDetectionNetwork, setIouThreshold))
        ;

    // SystemLogger node
    py::class_<SystemLogger, Node, std::shared_ptr<SystemLogger>>(m, "SystemLogger", DOC(dai, node, SystemLogger))
        .def_readonly("out", &SystemLogger::out, DOC(dai, node, SystemLogger, out))
        .def("setRate", &SystemLogger::setRate, py::arg("hz"), DOC(dai, node, SystemLogger, setRate))
        ;


    ////////////////////////////////////
    // Node properties bindings
    ////////////////////////////////////
    py::class_<ColorCameraProperties> colorCameraProperties(m, "ColorCameraProperties");
    colorCameraProperties
        .def_readwrite("initialControl", &ColorCameraProperties::initialControl)
        .def_readwrite("boardSocket", &ColorCameraProperties::boardSocket)
        .def_readwrite("colorOrder", &ColorCameraProperties::colorOrder)
        .def_readwrite("interleaved", &ColorCameraProperties::interleaved)
        .def_readwrite("previewHeight", &ColorCameraProperties::previewHeight)
        .def_readwrite("previewWidth", &ColorCameraProperties::previewWidth)
        .def_readwrite("videoHeight", &ColorCameraProperties::videoHeight)
        .def_readwrite("videoWidth", &ColorCameraProperties::videoWidth)
        .def_readwrite("stillHeight", &ColorCameraProperties::stillHeight)
        .def_readwrite("stillWidth", &ColorCameraProperties::stillWidth)
        .def_readwrite("resolution", &ColorCameraProperties::resolution)
        .def_readwrite("fps", &ColorCameraProperties::fps)
        .def_readwrite("sensorCropX", &ColorCameraProperties::sensorCropX)
        .def_readwrite("sensorCropY", &ColorCameraProperties::sensorCropY)
    ;

    py::enum_<ColorCameraProperties::SensorResolution>(colorCameraProperties, "SensorResolution")
        .value("THE_1080_P", ColorCameraProperties::SensorResolution::THE_1080_P)
        .value("THE_4_K", ColorCameraProperties::SensorResolution::THE_4_K)
        .value("THE_12_MP", ColorCameraProperties::SensorResolution::THE_12_MP)
        ;

    py::enum_<ColorCameraProperties::ColorOrder>(colorCameraProperties, "ColorOrder")
        .value("BGR", ColorCameraProperties::ColorOrder::BGR)
        .value("RGB", ColorCameraProperties::ColorOrder::RGB)
        ;
    // ALIAS
    m.attr("ColorCamera").attr("Properties") = colorCameraProperties;

        

    // MonoCamera props
    py::class_<MonoCameraProperties> monoCameraProperties(m, "MonoCameraProperties");
    monoCameraProperties
        .def_readwrite("initialControl", &MonoCameraProperties::initialControl)
        .def_readwrite("boardSocket", &MonoCameraProperties::boardSocket)
        .def_readwrite("resolution", &MonoCameraProperties::resolution)
        .def_readwrite("fps",  &MonoCameraProperties::fps)
    ;

    py::enum_<MonoCameraProperties::SensorResolution>(monoCameraProperties, "SensorResolution")
        .value("THE_720_P", MonoCameraProperties::SensorResolution::THE_720_P)
        .value("THE_800_P", MonoCameraProperties::SensorResolution::THE_800_P)
        .value("THE_400_P", MonoCameraProperties::SensorResolution::THE_400_P)
        ;
    // ALIAS
    m.attr("MonoCamera").attr("Properties") = monoCameraProperties;
   

    // StereoDepth props
    py::class_<StereoDepthProperties> stereoDepthProperties(m, "StereoDepthProperties");
    stereoDepthProperties
        .def_readwrite("calibration",             &StereoDepthProperties::calibration)
        .def_readwrite("median",                  &StereoDepthProperties::median)
        .def_readwrite("confidenceThreshold",     &StereoDepthProperties::confidenceThreshold)
        .def_readwrite("enableLeftRightCheck",    &StereoDepthProperties::enableLeftRightCheck)
        .def_readwrite("enableSubpixel",          &StereoDepthProperties::enableSubpixel)
        .def_readwrite("enableExtendedDisparity", &StereoDepthProperties::enableExtendedDisparity)
        .def_readwrite("rectifyMirrorFrame",      &StereoDepthProperties::rectifyMirrorFrame)
        .def_readwrite("rectifyEdgeFillColor",    &StereoDepthProperties::rectifyEdgeFillColor)
        .def_readwrite("enableOutputRectified",   &StereoDepthProperties::enableOutputRectified)
        .def_readwrite("enableOutputDepth",       &StereoDepthProperties::enableOutputDepth)
        .def_readwrite("width",                   &StereoDepthProperties::width)
        .def_readwrite("height",                  &StereoDepthProperties::height)
        ;

    py::enum_<StereoDepthProperties::MedianFilter>(stereoDepthProperties, "MedianFilter")
        .value("MEDIAN_OFF", StereoDepthProperties::MedianFilter::MEDIAN_OFF)
        .value("KERNEL_3x3", StereoDepthProperties::MedianFilter::KERNEL_3x3)
        .value("KERNEL_5x5", StereoDepthProperties::MedianFilter::KERNEL_5x5)
        .value("KERNEL_7x7", StereoDepthProperties::MedianFilter::KERNEL_7x7)
        ;
    // ALIAS
    m.attr("StereoDepth").attr("Properties") = stereoDepthProperties;
   


    // VideoEncoder props
    py::class_<VideoEncoderProperties> videoEncoderProperties(m, "VideoEncoderProperties");
    videoEncoderProperties
        .def_readwrite("bitrate", &VideoEncoderProperties::bitrate)
        .def_readwrite("keyframeFrequency", &VideoEncoderProperties::keyframeFrequency)
        .def_readwrite("maxBitrate", &VideoEncoderProperties::maxBitrate)
        .def_readwrite("numBFrames", &VideoEncoderProperties::numBFrames)
        .def_readwrite("numFramesPool", &VideoEncoderProperties::numFramesPool)
        .def_readwrite("profile", &VideoEncoderProperties::profile)
        .def_readwrite("quality", &VideoEncoderProperties::quality)
        .def_readwrite("rateCtrlMode", &VideoEncoderProperties::rateCtrlMode)
        .def_readwrite("width", &VideoEncoderProperties::width)
        .def_readwrite("height", &VideoEncoderProperties::height)
        ;

    py::enum_<VideoEncoderProperties::Profile>(videoEncoderProperties, "Profile")
        .value("H264_BASELINE", VideoEncoderProperties::Profile::H264_BASELINE)
        .value("H264_HIGH", VideoEncoderProperties::Profile::H264_HIGH)
        .value("H264_MAIN", VideoEncoderProperties::Profile::H264_MAIN)
        .value("H265_MAIN", VideoEncoderProperties::Profile::H265_MAIN)
        .value("MJPEG", VideoEncoderProperties::Profile::MJPEG)
        ;

    py::enum_<VideoEncoderProperties::RateControlMode>(videoEncoderProperties, "RateControlMode")
        .value("CBR", VideoEncoderProperties::RateControlMode::CBR)
        .value("VBR", VideoEncoderProperties::RateControlMode::VBR)
        ;     
    // ALIAS
    m.attr("VideoEncoder").attr("Properties") = videoEncoderProperties;




    py::class_<SystemLoggerProperties>(m, "SystemLoggerProperties")
        .def_readwrite("rateHz", &SystemLoggerProperties::rateHz)
        ;

    

}
