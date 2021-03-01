#include "CommonBindings.hpp"

// depthai-shared
#include "depthai-shared/common/CameraBoardSocket.hpp"
#include "depthai-shared/common/CameraImageOrientation.hpp"
#include "depthai-shared/common/MemoryInfo.hpp"
#include "depthai-shared/common/ChipTemperature.hpp"
#include "depthai-shared/common/CpuUsage.hpp"

void CommonBindings::bind(pybind11::module& m){

    using namespace dai;
    
    // CameraBoardSocket enum bindings
    py::enum_<CameraBoardSocket>(m, "CameraBoardSocket")
        .value("AUTO", CameraBoardSocket::AUTO)
        .value("RGB", CameraBoardSocket::RGB)
        .value("LEFT", CameraBoardSocket::LEFT)
        .value("RIGHT", CameraBoardSocket::RIGHT)
    ;
    
    // CameraImageOrientation enum bindings
    py::enum_<CameraImageOrientation>(m, "CameraImageOrientation")
        .value("AUTO", CameraImageOrientation::AUTO)
        .value("NORMAL", CameraImageOrientation::NORMAL)
        .value("HORIZONTAL_MIRROR", CameraImageOrientation::HORIZONTAL_MIRROR)
        .value("VERTICAL_FLIP", CameraImageOrientation::VERTICAL_FLIP)
        .value("ROTATE_180_DEG", CameraImageOrientation::ROTATE_180_DEG)
    ;

    // MemoryInfo
    py::class_<MemoryInfo>(m, "MemoryInfo")
        .def(py::init<>())
        .def_readwrite("remaining", &MemoryInfo::remaining)
        .def_readwrite("used", &MemoryInfo::used)
        .def_readwrite("total", &MemoryInfo::total)
    ;
     
    // ChipTemperature
    py::class_<ChipTemperature>(m, "ChipTemperature")
        .def(py::init<>())
        .def_readwrite("css", &ChipTemperature::css)
        .def_readwrite("mss", &ChipTemperature::mss)
        .def_readwrite("upa", &ChipTemperature::upa)
        .def_readwrite("dss", &ChipTemperature::dss)
        .def_readwrite("average", &ChipTemperature::average)
    ;
    
    // CpuUsage
    py::class_<CpuUsage>(m, "CpuUsage")
        .def(py::init<>())
        .def_readwrite("average", &CpuUsage::average)
        .def_readwrite("msTime", &CpuUsage::msTime)
    ;

}
