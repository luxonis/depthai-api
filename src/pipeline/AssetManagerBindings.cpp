#include "AssetManagerBindings.hpp"

// depthai
#include "depthai/pipeline/AssetManager.hpp"

void AssetManagerBindings::bind(pybind11::module& m){

    using namespace dai;

    // Bind Asset
    py::class_<Asset, std::shared_ptr<Asset>>(m, "Asset", DOC(dai, Asset))
        .def(py::init<>())
        .def(py::init<std::string>())
        .def_readonly("key", &Asset::key)
        // numpy array access - zero copy on access
        .def_property("data", [](py::object &obj){
            dai::Asset &a = obj.cast<dai::Asset&>();
            return py::array_t<std::uint8_t>(a.data.size(), a.data.data(), obj);
        }, [](py::object &obj, py::array_t<std::uint8_t, py::array::c_style> array){
            dai::Asset &a = obj.cast<dai::Asset&>();
            a.data = {array.data(), array.data() + array.size()};
        })
        .def_readwrite("alignment", &Asset::alignment)
    ;


    // Bind AssetManager
    py::class_<AssetManager>(m, "AssetManager", DOC(dai, AssetManager))
        .def(py::init<>())
        .def("addExisting", &AssetManager::addExisting, py::arg("assets"), DOC(dai, AssetManager, addExisting))
        .def("add", static_cast<void (AssetManager::*)(Asset)>(&AssetManager::add), py::arg("asset"), DOC(dai, AssetManager, add))
        .def("add", static_cast<void (AssetManager::*)(const std::string&, Asset)>(&AssetManager::add), py::arg("key"), py::arg("asset"), DOC(dai, AssetManager, add, 2))
        .def("set", &AssetManager::set, py::arg("key"), py::arg("asset"), DOC(dai, AssetManager, set))        
        .def("get", static_cast<std::shared_ptr<const Asset> (AssetManager::*)(const std::string&) const>(&AssetManager::get), py::arg("key"), DOC(dai, AssetManager, get))
        .def("get", static_cast<std::shared_ptr<Asset> (AssetManager::*)(const std::string&)>(&AssetManager::get), py::arg("key"), DOC(dai, AssetManager, get, 2))
        .def("getAll", static_cast<std::vector<std::shared_ptr<const Asset>> (AssetManager::*)() const>(&AssetManager::getAll), DOC(dai, AssetManager, getAll))
        .def("getAll", static_cast<std::vector<std::shared_ptr<Asset>> (AssetManager::*)()>(&AssetManager::getAll), DOC(dai, AssetManager, getAll, 2))
        .def("size", &AssetManager::size, DOC(dai, AssetManager, size))
        .def("remove", &AssetManager::remove, py::arg("key"), DOC(dai, AssetManager, remove))
    ;

}