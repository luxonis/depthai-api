#include "CalibrationHandlerBindings.hpp"
#include "depthai/device/CalibrationHandler.hpp"
#include "depthai-shared/common/Point2f.hpp"
#include <vector>

void CalibrationHandlerBindings::bind(pybind11::module& m){

    using namespace dai;

    // bind pipeline
    py::class_<CalibrationHandler>(m, "CalibrationHandler", DOC(dai, CalibrationHandler))
        .def(py::init<>(), DOC(dai, CalibrationHandler, CalibrationHandler, 1))
        .def(py::init<std::string>(), DOC(dai, CalibrationHandler, CalibrationHandler, 2))
        .def(py::init<std::string, std::string>(), DOC(dai, CalibrationHandler, CalibrationHandler, 3))
        .def(py::init<EepromData>(), DOC(dai, CalibrationHandler, CalibrationHandler, 4))
        
        // .def("getCameraIntrinsics", [](){CameraS} , DOC(dai, Device, getCameraIntrinsics, 0))
        .def("getCameraIntrinsics", py::overload_cast<CameraBoardSocket, int, int, Point2f, Point2f>(&CalibrationHandler::getCameraIntrinsics), py::arg("cameraId"), py::arg("resizeWidth") = -1, py::arg("resizeHeight") = -1, py::arg("topLeftPixelId") = Point2f(), py::arg("bottomRightPixelId") = Point2f(), DOC(dai, Device, getCameraIntrinsics, 0))
        .def("getCameraIntrinsics", py::overload_cast<CameraBoardSocket, Size2f, Point2f, Point2f>(&CalibrationHandler::getCameraIntrinsics), py::arg("cameraId"), py::arg("destShape") = Size2f(-1, -1), py::arg("topLeftPixelId") = Point2f(), py::arg("bottomRightPixelId") = Point2f(), DOC(dai, Device, getCameraIntrinsics, 1))

        // .def("getCameraIntrinsics", &CalibrationHandler::getCameraIntrinsics, py::arg("cameraId"), py::arg("resizeWidth") = -1, py::arg("resizeHeight") = -1, py::arg("topLeftPixelId") = Point2f(), py::arg("bottomRightPixelId") = Point2f(), DOC(dai, Device, getCameraIntrinsics, 0))
        // .def("getCameraIntrinsics", &CalibrationHandler::getCameraIntrinsics, py::arg("cameraId"), py::arg("destShape") = Size2f(-1, -1), py::arg("topLeftPixelId") = Point2f(), py::arg("bottomRightPixelId") = Point2f(), DOC(dai, Device, getCameraIntrinsics, 1))
        .def("getDefaultIntrinsics", &CalibrationHandler::getDefaultIntrinsics, py::arg("cameraId"), DOC(dai, Device, getDefaultIntrinsics))

        .def("getDistortionCoefficients", &CalibrationHandler::getDistortionCoefficients, py::arg("cameraId"), DOC(dai, Device, getDistortionCoefficients))
        .def("getCameraExtrinsics", &CalibrationHandler::getCameraExtrinsics, py::arg("srcCamera"), py::arg("dstCamera"), py::arg("useMeasuredTranslation") = false, DOC(dai, Device, getCameraExtrinsics))

        .def("getCameraToImuExtrinsics", &CalibrationHandler::getCameraToImuExtrinsics, py::arg("cameraId"), py::arg("useMeasuredTranslation") = false, DOC(dai, Device, getCameraToImuExtrinsics))
        .def("getImuToCameraExtrinsics", &CalibrationHandler::getImuToCameraExtrinsics, py::arg("cameraId"), py::arg("useMeasuredTranslation") = false, DOC(dai, Device, getImuToCameraExtrinsics))
        .def("eepromToJsonFile", &CalibrationHandler::eepromToJsonFile, py::arg("destPath"), DOC(dai, Device, eepromToJsonFile))
        
        .def("setBoardInfo", &CalibrationHandler::setBoardInfo, py::arg("swapLeftRightCam"), py::arg("boardName"), py::arg("boardRev"), DOC(dai, Device, setBoardInfo))
        // .def("setCameraIntrinsics", &CalibrationHandler::setCameraIntrinsics, py::arg("cameraId"), py::arg("intrinsics"), py::arg("width"), py::arg("height"), DOC(dai, Device, setCameraIntrinsics, 1))
        // .def("setCameraIntrinsics", &CalibrationHandler::setCameraIntrinsics, py::arg("cameraId"), py::arg("intrinsics"), py::arg("frameSize"), DOC(dai, Device, setCameraIntrinsics, 0))
        
        .def("setCameraIntrinsics", py::overload_cast<CameraBoardSocket, std::vector<std::vector<float>>, Size2f>(&CalibrationHandler::setCameraIntrinsics), py::arg("cameraId"), py::arg("intrinsics"), py::arg("frameSize"), DOC(dai, Device, setCameraIntrinsics, 0))
        .def("setCameraIntrinsics", py::overload_cast<CameraBoardSocket, std::vector<std::vector<float>>, int, int>(&CalibrationHandler::setCameraIntrinsics), py::arg("cameraId"), py::arg("intrinsics"), py::arg("width"), py::arg("height"), DOC(dai, Device, setCameraIntrinsics, 1))

        .def("setdistortionCoefficients", &CalibrationHandler::setdistortionCoefficients, py::arg("cameraId"), py::arg("distortionCoefficients"), DOC(dai, Device, setdistortionCoefficients))
        .def("setFov", &CalibrationHandler::setFov, py::arg("cameraId"), py::arg("hfov"), DOC(dai, Device, setFov))
        
        .def("setCameraExtrinsics", &CalibrationHandler::setCameraExtrinsics, py::arg("srcCameraId"), py::arg("destCameraId"), py::arg("rotationMatrix"), py::arg("translation"), py::arg("measuredTranslation") = std::vector<float>(3,0), DOC(dai, Device, setCameraExtrinsics))
        .def("setImuExtrinsics", &CalibrationHandler::setImuExtrinsics, py::arg("destCameraId"), py::arg("rotationMatrix"), py::arg("translation"), py::arg("measuredTranslation") = std::vector<float>(3,0), DOC(dai, Device, setImuExtrinsics))

        .def("setStereoLeft", &CalibrationHandler::setStereoLeft, py::arg("cameraId"), py::arg("rectifiedRotation"), DOC(dai, Device, setStereoLeft))
        .def("setStereoRight", &CalibrationHandler::setStereoRight, py::arg("cameraId"), py::arg("rectifiedRotation"), DOC(dai, Device, setStereoRight))
        .def("getStereoLeftRectificationRotation", &CalibrationHandler::getStereoLeftRectificationRotation, DOC(dai, Device, getStereoLeftRectificationRotation))
        .def("getStereoRightRectificationRotation", &CalibrationHandler::getStereoRightRectificationRotation, DOC(dai, Device, getStereoRightRectificationRotation))

        .def("getEepromData", &CalibrationHandler::getEepromData, DOC(dai, Device, getEepromData));

}
