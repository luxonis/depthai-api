#include "XLinkConnectionBindings.hpp"

#include "depthai/xlink/XLinkConnection.hpp"

#include <cmath>
#include <cstring>

void XLinkConnectionBindings::bind(pybind11::module& m){

    using namespace dai;

    py::class_<DeviceInfo>(m, "DeviceInfo")
        .def(py::init<>())
        .def_readwrite("desc", &DeviceInfo::desc)
        .def_readwrite("state", &DeviceInfo::state)
        .def("getMxId", &DeviceInfo::getMxId)
        ;

    py::class_<deviceDesc_t>(m, "DeviceDesc")
        .def(py::init<>())
        .def_readwrite("protocol", &deviceDesc_t::protocol)
        .def_readwrite("platform", &deviceDesc_t::platform)
        .def_property("name", 
            [](deviceDesc_t& o){return std::string(o.name);},
            [](deviceDesc_t& o, std::string n){ std::strncpy(o.name, n.c_str(), std::min(XLINK_MAX_NAME_SIZE,(int) n.size()));}
        )
        ;

    py::enum_<XLinkDeviceState_t>(m, "XLinkDeviceState")
        .value("X_LINK_ANY_STATE", X_LINK_ANY_STATE)
        .value("X_LINK_BOOTED", X_LINK_BOOTED)
        .value("X_LINK_UNBOOTED", X_LINK_UNBOOTED)
        .value("X_LINK_BOOTLOADER", X_LINK_BOOTLOADER)
        .export_values();
        ;


    py::enum_<XLinkProtocol_t>(m, "XLinkProtocol")
        .value("X_LINK_USB_VSC", X_LINK_USB_VSC)
        .value("X_LINK_USB_CDC", X_LINK_USB_CDC)
        .value("X_LINK_PCIE", X_LINK_PCIE)
        .value("X_LINK_IPC", X_LINK_IPC)
        .value("X_LINK_NMB_OF_PROTOCOLS", X_LINK_NMB_OF_PROTOCOLS)
        .value("X_LINK_ANY_PROTOCOL", X_LINK_ANY_PROTOCOL)
        .export_values()
        ;

    py::enum_<XLinkPlatform_t>(m, "XLinkPlatform")
        .value("X_LINK_ANY_PLATFORM", X_LINK_ANY_PLATFORM)
        .value("X_LINK_MYRIAD_2", X_LINK_MYRIAD_2)
        .value("X_LINK_MYRIAD_X", X_LINK_MYRIAD_X)
        .export_values()
        ;

    py::class_<XLinkConnection>(m, "XLinkConnection")
        .def(py::init<const DeviceInfo&, std::vector<std::uint8_t>>())
        .def(py::init<const DeviceInfo&, std::string>())
        .def(py::init<const DeviceInfo&>())
        .def_static("getAllConnectedDevices", &XLinkConnection::getAllConnectedDevices, py::arg("state") = X_LINK_ANY_STATE)
        .def_static("getFirstDevice", &XLinkConnection::getFirstDevice, py::arg("state") = X_LINK_ANY_STATE)
        .def_static("getDeviceByMxId", &XLinkConnection::getDeviceByMxId, py::arg("mxId"), py::arg("state") = X_LINK_ANY_STATE)
        ;


}