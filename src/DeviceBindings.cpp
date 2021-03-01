#include "DeviceBindings.hpp"

// depthai
#include "depthai/device/Device.hpp"

// std::chrono bindings
#include <pybind11/chrono.h>
// py::detail
#include <pybind11/detail/common.h>

// Searches for available devices (as Device constructor)
// but pooling, to check for python interrupts, and releases GIL in between
static std::unique_ptr<dai::Device> deviceConstructorHelper(const dai::Pipeline& pipeline, const std::string& pathToCmd = "", bool usb2Mode = false){
    auto startTime = std::chrono::steady_clock::now();
    bool found;
    dai::DeviceInfo deviceInfo = {};
    do {
        {          
            // releases python GIL
            py::gil_scoped_release release;
            std::tie(found, deviceInfo) = dai::Device::getFirstAvailableDevice();
            // Check if found
            if(found){
                break;
            } else {
                // block for 100ms                    
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
        }
        // reacquires python GIL for PyErr_CheckSignals call
        // check if interrupt triggered in between
        if (PyErr_CheckSignals() != 0) throw py::error_already_set();
    } while(std::chrono::steady_clock::now() - startTime < dai::Device::DEFAULT_SEARCH_TIME);

    // If neither UNBOOTED nor BOOTLOADER were found (after 'DEFAULT_SEARCH_TIME'), try BOOTED
    if(!found) std::tie(found, deviceInfo) = dai::XLinkConnection::getFirstDevice(X_LINK_BOOTED);

    // if no devices found, then throw
    if(!found) throw std::runtime_error("No available devices");

    // Check if pathToCmd supplied
    if(pathToCmd.empty()){
        return std::unique_ptr<dai::Device>(new dai::Device(pipeline, deviceInfo, usb2Mode));
    } else {
        return std::unique_ptr<dai::Device>(new dai::Device(pipeline, deviceInfo, pathToCmd));
    }
    return nullptr;
} 


std::vector<std::string> deviceGetQueueEventsHelper(dai::Device& d, const std::vector<std::string>& queueNames, std::size_t maxNumEvents, std::chrono::microseconds timeout){
    using namespace std::chrono;

    // if timeout < 0, unlimited timeout
    bool unlimitedTimeout = timeout < microseconds(0);
    auto startTime = steady_clock::now();
    do {
        {          
            // releases python GIL
            py::gil_scoped_release release;
            // block for 100ms
            auto events = d.getQueueEvents(queueNames, maxNumEvents, std::chrono::milliseconds(100));
            if(!events.empty()) return events;
        }
        // reacquires python GIL for PyErr_CheckSignals call
        // check if interrupt triggered in between
        if (PyErr_CheckSignals() != 0) throw py::error_already_set();
    } while(unlimitedTimeout || steady_clock::now() - startTime < timeout);
    
    return std::vector<std::string>(); 
}


void DeviceBindings::bind(pybind11::module& m){

    using namespace dai;


    // Bind Device, using DeviceWrapper to be able to destruct the object by calling close()
    py::class_<Device>(m, "Device")
        // Python only methods
        .def("__enter__", [](py::object obj){ return obj; })
        .def("__exit__", [](Device& d, py::object type, py::object value, py::object traceback) { d.close(); })
        .def("close", &Device::close, "Closes the connection to device. Better alternative is the usage of context manager: `with depthai.Device(pipeline) as device:`")

        //dai::Device methods
        //static (no need for the wrapper)
        .def_static("getAnyAvailableDevice", [](std::chrono::microseconds us){ return Device::getAnyAvailableDevice(us); }, py::arg("timeout"), DOC(dai, Device, getAnyAvailableDevice))
        .def_static("getAnyAvailableDevice", [](){ return Device::getAnyAvailableDevice(); }, DOC(dai, Device, getAnyAvailableDevice, 2))
        .def_static("getFirstAvailableDevice", &Device::getFirstAvailableDevice, DOC(dai, Device, getFirstAvailableDevice))
        .def_static("getAllAvailableDevices", &Device::getAllAvailableDevices, DOC(dai, Device, getAllAvailableDevices))
        .def_static("getEmbeddedDeviceBinary", &Device::getEmbeddedDeviceBinary, py::arg("usb2Mode"), py::arg("version") = Pipeline::DEFAULT_OPENVINO_VERSION, DOC(dai, Device, getEmbeddedDeviceBinary))
        .def_static("getDeviceByMxId", &Device::getDeviceByMxId, py::arg("mxId"), DOC(dai, Device, getDeviceByMxId))
        
        // methods
        .def(py::init([](const Pipeline& pipeline){ return deviceConstructorHelper(pipeline); }), py::arg("pipeline"), DOC(dai, Device, Device))
        .def(py::init([](const Pipeline& pipeline, bool usb2Mode){ 
            // Blocking constructor
            return deviceConstructorHelper(pipeline, std::string(""), usb2Mode); 
        }), py::arg("pipeline"), py::arg("usb2Mode"), DOC(dai, Device, Device, 2))
        .def(py::init([](const Pipeline& pipeline, const std::string& pathToCmd){
            // Blocking constructor
            return deviceConstructorHelper(pipeline, pathToCmd); 
        }), py::arg("pipeline"), py::arg("pathToCmd"), DOC(dai, Device, Device, 3))
        .def(py::init([](const Pipeline& pipeline, const DeviceInfo& deviceInfo, bool usb2Mode){
            // Non blocking constructor
            return std::unique_ptr<Device>(new Device(pipeline, deviceInfo, usb2Mode));
        }), py::arg("pipeline"), py::arg("deviceDesc"), py::arg("usb2Mode") = false, DOC(dai, Device, Device, 4))
        .def(py::init([](const Pipeline& pipeline, const DeviceInfo& deviceInfo, std::string pathToCmd){
            // Non blocking constructor
            return std::unique_ptr<Device>(new Device(pipeline, deviceInfo, pathToCmd));
        }), py::arg("pipeline"), py::arg("deviceDesc"), py::arg("pathToCmd"), DOC(dai, Device, Device, 5))

        .def("isPipelineRunning", &Device::isPipelineRunning, DOC(dai, Device, isPipelineRunning))
        .def("startPipeline", &Device::startPipeline, DOC(dai, Device, startPipeline))

        .def("getOutputQueue", static_cast<std::shared_ptr<DataOutputQueue>(Device::*)(const std::string&)>(&Device::getOutputQueue), py::arg("name"), DOC(dai, Device, getOutputQueue))
        .def("getOutputQueue", static_cast<std::shared_ptr<DataOutputQueue>(Device::*)(const std::string&, unsigned int, bool)>(&Device::getOutputQueue), py::arg("name"), py::arg("maxSize"), py::arg("blocking") = true, DOC(dai, Device, getOutputQueue, 2))
        .def("getOutputQueueNames", &Device::getOutputQueueNames, DOC(dai, Device, getOutputQueueNames))

        .def("getInputQueue", static_cast<std::shared_ptr<DataInputQueue>(Device::*)(const std::string&)>(&Device::getInputQueue), py::arg("name"), DOC(dai, Device, getInputQueue))
        .def("getInputQueue", static_cast<std::shared_ptr<DataInputQueue>(Device::*)(const std::string&, unsigned int, bool)>(&Device::getInputQueue), py::arg("name"), py::arg("maxSize"), py::arg("blocking") = true, DOC(dai, Device, getInputQueue, 2))
        .def("getInputQueueNames", &Device::getInputQueueNames, DOC(dai, Device, getInputQueueNames))

        .def("getQueueEvents", [](Device& d, const std::vector<std::string>& queueNames, std::size_t maxNumEvents, std::chrono::microseconds timeout) {
            return deviceGetQueueEventsHelper(d, queueNames, maxNumEvents, timeout);
        }, py::arg("queueNames"), py::arg("maxNumEvents") = std::numeric_limits<std::size_t>::max(), py::arg("timeout") = std::chrono::microseconds(-1), DOC(dai, Device, getQueueEvents))
        .def("getQueueEvents", [](Device& d, std::string queueName, std::size_t maxNumEvents, std::chrono::microseconds timeout) {
            return deviceGetQueueEventsHelper(d, std::vector<std::string>{queueName}, maxNumEvents, timeout);
        }, py::arg("queueName"), py::arg("maxNumEvents") = std::numeric_limits<std::size_t>::max(), py::arg("timeout") = std::chrono::microseconds(-1), DOC(dai, Device, getQueueEvents, 3))
        .def("getQueueEvents", [](Device& d, std::size_t maxNumEvents, std::chrono::microseconds timeout) {
            return deviceGetQueueEventsHelper(d, d.getOutputQueueNames(), maxNumEvents, timeout);
        }, py::arg("maxNumEvents") = std::numeric_limits<std::size_t>::max(), py::arg("timeout") = std::chrono::microseconds(-1), DOC(dai, Device, getQueueEvents, 4))

        .def("getQueueEvent", [](Device& d, const std::vector<std::string>& queueNames, std::chrono::microseconds timeout) {
            auto events = deviceGetQueueEventsHelper(d, queueNames, std::numeric_limits<std::size_t>::max(), timeout);
            if(events.empty()) return std::string("");
            return events[0];
        }, py::arg("queueNames"), py::arg("timeout") = std::chrono::microseconds(-1), DOC(dai, Device, getQueueEvent))
        
        .def("getQueueEvent", [](Device& d, std::string queueName, std::chrono::microseconds timeout) {
            auto events = deviceGetQueueEventsHelper(d, std::vector<std::string>{queueName}, std::numeric_limits<std::size_t>::max(), timeout);
            if(events.empty()) return std::string("");
            return events[0];
        }, py::arg("queueName"), py::arg("timeout") = std::chrono::microseconds(-1), DOC(dai, Device, getQueueEvent, 3))
        
        .def("getQueueEvent", [](Device& d, std::chrono::microseconds timeout) {
            auto events = deviceGetQueueEventsHelper(d, d.getOutputQueueNames(), std::numeric_limits<std::size_t>::max(), timeout);
            if(events.empty()) return std::string("");
            return events[0];
        }, py::arg("timeout") = std::chrono::microseconds(-1), DOC(dai, Device, getQueueEvent, 4))

        //.def("setCallback", DeviceWrapper::wrap(&Device::setCallback), py::arg("name"), py::arg("callback"))
        .def("setLogLevel", &Device::setLogLevel, py::arg("level"), DOC(dai, Device, setLogLevel))
        .def("getLogLevel", &Device::getLogLevel, DOC(dai, Device, getLogLevel))
        .def("setSystemInformationLoggingRate", &Device::setSystemInformationLoggingRate, py::arg("rateHz"), DOC(dai, Device, setSystemInformationLoggingRate))
        .def("getSystemInformationLoggingRate", &Device::getSystemInformationLoggingRate, DOC(dai, Device, getSystemInformationLoggingRate))
        .def("getDdrMemoryUsage", &Device::getDdrMemoryUsage, DOC(dai, Device, getDdrMemoryUsage))
        .def("getCmxMemoryUsage", &Device::getCmxMemoryUsage, DOC(dai, Device, getCmxMemoryUsage))
        .def("getLeonCssHeapUsage", &Device::getLeonCssHeapUsage, DOC(dai, Device, getLeonCssHeapUsage))
        .def("getLeonMssHeapUsage", &Device::getLeonMssHeapUsage, DOC(dai, Device, getLeonMssHeapUsage))
        .def("getChipTemperature", &Device::getChipTemperature, DOC(dai, Device, getChipTemperature))
        .def("getLeonCssCpuUsage", &Device::getLeonCssCpuUsage, DOC(dai, Device, getLeonCssCpuUsage))
        .def("getLeonMssCpuUsage", &Device::getLeonMssCpuUsage, DOC(dai, Device, getLeonMssCpuUsage))
        .def("setLogOutputLevel", &Device::setLogOutputLevel, py::arg("level"), DOC(dai, Device, setLogOutputLevel))
        .def("getLogOutputLevel", &Device::getLogOutputLevel, DOC(dai, Device, getLogOutputLevel))
        .def("addLogCallback", &Device::addLogCallback, py::arg("callback"), DOC(dai, Device, addLogCallback))
        .def("removeLogCallback", &Device::removeLogCallback, py::arg("callbackId"), DOC(dai, Device, removeLogCallback))
        ;

}