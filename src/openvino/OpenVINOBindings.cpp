#include "OpenVINOBindings.hpp"

// depthai
#include "depthai/openvino/OpenVINO.hpp"

void OpenVINOBindings::bind(pybind11::module& m){

    using namespace dai;

    // Bind OpenVINO
    py::class_<OpenVINO> openvino(m, "OpenVINO", DOC(dai, OpenVINO));
    openvino
        .def_static("getVersions", &OpenVINO::getVersions, DOC(dai, OpenVINO, getVersions))
        .def_static("getVersionName", &OpenVINO::getVersionName, py::arg("version"), DOC(dai, OpenVINO, getVersionName))
        .def_static("parseVersionName", &OpenVINO::parseVersionName, py::arg("versionString"), DOC(dai, OpenVINO, parseVersionName))
        .def_static("getBlobSupportedVersions", &OpenVINO::getBlobSupportedVersions, py::arg("majorVersion"), py::arg("majorVersion"), DOC(dai, OpenVINO, getBlobSupportedVersions))
        .def_static("getBlobLatestSupportedVersion", &OpenVINO::getBlobLatestSupportedVersion, py::arg("majorVersion"), py::arg("majorVersion"), DOC(dai, OpenVINO, getBlobLatestSupportedVersion))
        .def_static("areVersionsBlobCompatible", &OpenVINO::areVersionsBlobCompatible, py::arg("v1"), py::arg("v2"), DOC(dai, OpenVINO, areVersionsBlobCompatible))
    ;

    // not strongly typed enum OpenVINO::Version
    // previous step defined class 'OpenVINO' (variable 'openvino') 
    // which is used in defining the following enum (its scope)
    // and that the values are available directly under OpenVINO.VERSION_2020_1, ...
    // they are exported
    // By default, pybind creates strong typed enums, eg: OpenVINO::Version::VERSION_2020_1 
    py::enum_<OpenVINO::Version>(openvino, "Version", DOC(dai, OpenVINO, Version))
        .value("VERSION_2020_1", OpenVINO::Version::VERSION_2020_1)
        .value("VERSION_2020_2", OpenVINO::Version::VERSION_2020_2)
        .value("VERSION_2020_3", OpenVINO::Version::VERSION_2020_3)
        .value("VERSION_2020_4", OpenVINO::Version::VERSION_2020_4)
        .value("VERSION_2021_1", OpenVINO::Version::VERSION_2021_1)
        .value("VERSION_2021_2", OpenVINO::Version::VERSION_2021_2)
        .value("VERSION_2021_3", OpenVINO::Version::VERSION_2021_3)
        .export_values()
    ;

}



