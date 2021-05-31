
#include <exception>
#include <fstream>
#include <iostream>
#include <list>
#include <memory>
#include <string>
#include <vector>

// pybind11
#include "pybind11_common.hpp"

// depthai-core
#include "depthai/build/version.hpp"

// project
#include "depthai/depthai.hpp"
#include "pipeline/AssetManagerBindings.hpp"
#include "pipeline/PipelineBindings.hpp"
#include "pipeline/CommonBindings.hpp"
#include "pipeline/NodeBindings.hpp"
#include "XLinkConnectionBindings.hpp"
#include "DeviceBindings.hpp"
#include "CalibrationHandlerBindings.hpp"
#include "DeviceBootloaderBindings.hpp"
#include "DatatypeBindings.hpp"
#include "DataQueueBindings.hpp"
#include "openvino/OpenVINOBindings.hpp"
#include "log/LogBindings.hpp"


PYBIND11_MODULE(depthai,m)
{

    // Depthai python version consists of: (depthai-core).(bindings revision)[+bindings hash]
    m.attr("__version__") = DEPTHAI_PYTHON_VERSION;
    m.attr("__commit__") = DEPTHAI_PYTHON_COMMIT_HASH;
    m.attr("__commit_datetime__") = DEPTHAI_PYTHON_COMMIT_DATETIME;
    m.attr("__build_datetime__") = DEPTHAI_PYTHON_BUILD_DATETIME;


    // Add bindings
    CommonBindings::bind(m);
    OpenVINOBindings::bind(m);
    AssetManagerBindings::bind(m);
    NodeBindings::bind(m);
    PipelineBindings::bind(m);
    XLinkConnectionBindings::bind(m);
    CalibrationHandlerBindings::bind(m);
    DeviceBindings::bind(m);
    DeviceBootloaderBindings::bind(m);
    DatatypeBindings::bind(m);
    DataQueueBindings::bind(m);
    LogBindings::bind(m);

    // Call dai::initialize on 'import depthai' to initialize asap with additional information to print
    dai::initialize(std::string("Python bindings - version: ") + DEPTHAI_PYTHON_VERSION + " from " + DEPTHAI_PYTHON_COMMIT_DATETIME + " build: " + DEPTHAI_PYTHON_BUILD_DATETIME);

}



