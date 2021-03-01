#include "PipelineBindings.hpp"

// depthai
#include "depthai/pipeline/Pipeline.hpp"

// depthai - nodes
#include "depthai/pipeline/node/XLinkIn.hpp"
#include "depthai/pipeline/node/XLinkOut.hpp"
#include "depthai/pipeline/node/NeuralNetwork.hpp"
#include "depthai/pipeline/node/ColorCamera.hpp"
#include "depthai/pipeline/node/VideoEncoder.hpp"
#include "depthai/pipeline/node/SPIOut.hpp"
#include "depthai/pipeline/node/ImageManip.hpp"
#include "depthai/pipeline/node/MonoCamera.hpp"
#include "depthai/pipeline/node/StereoDepth.hpp"
#include "depthai/pipeline/node/DetectionNetwork.hpp"
#include "depthai/pipeline/node/SystemLogger.hpp"

// depthai-shared
#include "depthai-shared/properties/GlobalProperties.hpp"

void PipelineBindings::bind(pybind11::module& m){

    using namespace dai;


    // Bind global properties
    py::class_<GlobalProperties>(m, "GlobalProperties")
        .def_readwrite("leonOsFrequencyHz", &GlobalProperties::leonCssFrequencyHz)
        .def_readwrite("leonRtFrequencyHz", &GlobalProperties::leonMssFrequencyHz)
        .def_readwrite("pipelineName", &GlobalProperties::pipelineName)
        .def_readwrite("pipelineVersion", &GlobalProperties::pipelineVersion)
        ;



    // bind pipeline
    py::class_<Pipeline>(m, "Pipeline", DOC(dai, Pipeline))
        .def(py::init<>(), DOC(dai, Pipeline, Pipeline))
        //.def(py::init<const Pipeline&>())
        .def("getGlobalProperties", &Pipeline::getGlobalProperties, DOC(dai, Pipeline, getGlobalProperties))
        //.def("create", &Pipeline::create<node::XLinkIn>)
        .def("remove", &Pipeline::remove, py::arg("node"), DOC(dai, Pipeline, remove))
        .def("getAllNodes", static_cast<std::vector<std::shared_ptr<const Node>> (Pipeline::*)() const>(&Pipeline::getAllNodes), py::return_value_policy::reference_internal, DOC(dai, Pipeline, getAllNodes))
        .def("getAllNodes", static_cast<std::vector<std::shared_ptr< Node>> (Pipeline::*)()>(&Pipeline::getAllNodes), py::return_value_policy::reference_internal, DOC(dai, Pipeline, getAllNodes))
        .def("getNode", static_cast<std::shared_ptr<const Node> (Pipeline::*)(Node::Id) const>(&Pipeline::getNode), py::return_value_policy::reference_internal, DOC(dai, Pipeline, getNode))
        .def("getNode", static_cast<std::shared_ptr<Node> (Pipeline::*)(Node::Id)>(&Pipeline::getNode), py::return_value_policy::reference_internal, DOC(dai, Pipeline, getNode))
        .def("getConnections", &Pipeline::getConnections, DOC(dai, Pipeline, getConnections), DOC(dai, Pipeline, getConnections))
        .def("getConnectionMap", &Pipeline::getConnectionMap, DOC(dai, Pipeline, getConnectionMap), py::return_value_policy::reference_internal, DOC(dai, Pipeline, getConnectionMap))
        .def("getNodeMap", &Pipeline::getNodeMap, DOC(dai, Pipeline, getNodeMap), py::return_value_policy::reference_internal, DOC(dai, Pipeline, getNodeMap))
        .def("link", &Pipeline::link, DOC(dai, Pipeline, link), DOC(dai, Pipeline, link))
        .def("unlink", &Pipeline::unlink, DOC(dai, Pipeline, unlink), DOC(dai, Pipeline, unlink))
        .def("getAllAssets", &Pipeline::getAllAssets, DOC(dai, Pipeline, getAllAssets))
        .def("getAssetManager", static_cast<const AssetManager& (Pipeline::*)() const>(&Pipeline::getAssetManager), py::return_value_policy::reference_internal, DOC(dai, Pipeline, getAssetManager))
        .def("getAssetManager", static_cast<AssetManager& (Pipeline::*)()>(&Pipeline::getAssetManager), py::return_value_policy::reference_internal, DOC(dai, Pipeline, getAssetManager))
        .def("setOpenVINOVersion", &Pipeline::setOpenVINOVersion, py::arg("version") = Pipeline::DEFAULT_OPENVINO_VERSION, DOC(dai, Pipeline, setOpenVINOVersion), DOC(dai, Pipeline, setOpenVINOVersion))


         // templated create<NODE> function 
        .def("createXLinkIn", &Pipeline::create<node::XLinkIn>)
        .def("createXLinkOut", &Pipeline::create<node::XLinkOut>)
        .def("createNeuralNetwork", &Pipeline::create<node::NeuralNetwork>)
        .def("createColorCamera", &Pipeline::create<node::ColorCamera>)
        .def("createVideoEncoder", &Pipeline::create<node::VideoEncoder>)
        .def("createSPIOut", &Pipeline::create<node::SPIOut>)
        .def("createImageManip", &Pipeline::create<node::ImageManip>)
        .def("createMonoCamera", &Pipeline::create<node::MonoCamera>)
        .def("createStereoDepth", &Pipeline::create<node::StereoDepth>)
        .def("createMobileNetDetectionNetwork", &Pipeline::create<node::MobileNetDetectionNetwork>)
        .def("createYoloDetectionNetwork", &Pipeline::create<node::YoloDetectionNetwork>)
        .def("createSystemLogger", &Pipeline::create<node::SystemLogger>)
        ;
    

}
