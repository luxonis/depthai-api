
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
#include "DeviceBootloaderBindings.hpp"
#include "DatatypeBindings.hpp"
#include "DataQueueBindings.hpp"
#include "openvino/OpenVINOBindings.hpp"
#include "log/LogBindings.hpp"


PYBIND11_MODULE(depthai,m)
{

    // Depthai python version consists of: (depthai-core).(bindings revision)[+bindings hash]
    m.attr("__version__") = DEPTHAI_PYTHON_VERSION;

    // Add bindings 
    OpenVINOBindings::bind(m);
    AssetManagerBindings::bind(m);
    NodeBindings::bind(m);
    PipelineBindings::bind(m);
    XLinkConnectionBindings::bind(m);
    DeviceBindings::bind(m);
    DeviceBootloaderBindings::bind(m);
    CommonBindings::bind(m);
    DatatypeBindings::bind(m);
    DataQueueBindings::bind(m);
    LogBindings::bind(m);

    // Call dai::initialize on 'import depthai' to initialize asap
    dai::initialize();

}



