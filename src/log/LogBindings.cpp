#include "LogBindings.hpp"

// depthai
#include "depthai-shared/log/LogLevel.hpp"

void LogBindings::bind(pybind11::module& m){

    using namespace dai;

    // Bind LogLevel
    py::enum_<LogLevel>(m, "LogLevel")
        .value("TRACE", LogLevel::TRACE)
        .value("DEBUG", LogLevel::DEBUG)
        .value("INFO", LogLevel::INFO)
        .value("WARN", LogLevel::WARN)
        .value("ERR", LogLevel::ERR)
        .value("CRITICAL", LogLevel::CRITICAL)
        .value("OFF", LogLevel::OFF)
    ;
     
}