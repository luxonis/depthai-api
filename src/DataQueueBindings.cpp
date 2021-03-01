#include "DataQueueBindings.hpp"

// std
#include <chrono>

// depthai
#include "depthai/device/DataQueue.hpp"

void DataQueueBindings::bind(pybind11::module& m){

    using namespace dai;
    using namespace std::chrono;

    // To prevent blocking whole python interpreter, blocking functions like 'get' and 'send' 
    // are pooled with a reasonable delay and check for python interrupt signal in between.

    // Bind DataOutputQueue
    py::class_<DataOutputQueue, std::shared_ptr<DataOutputQueue>>(m, "DataOutputQueue", DOC(dai, DataOutputQueue))
        .def("getName", &DataOutputQueue::getName, DOC(dai, DataOutputQueue, getName))

        .def("addCallback", static_cast<int(DataOutputQueue::*)(std::function<void(std::string, std::shared_ptr<ADatatype>)>)>(&DataOutputQueue::addCallback), py::arg("callback"), DOC(dai, DataOutputQueue, addCallback))
        .def("addCallback", static_cast<int(DataOutputQueue::*)(std::function<void(std::shared_ptr<ADatatype>)>)>(&DataOutputQueue::addCallback), py::arg("callback"), DOC(dai, DataOutputQueue, addCallback, 2))
        .def("addCallback", static_cast<int(DataOutputQueue::*)(std::function<void()>)>(&DataOutputQueue::addCallback), py::arg("callback"), DOC(dai, DataOutputQueue, addCallback, 3))
        .def("removeCallback", &DataOutputQueue::removeCallback, py::arg("callbackId"), DOC(dai, DataOutputQueue, removeCallback))

        .def("setBlocking", &DataOutputQueue::setBlocking, py::arg("blocking"), DOC(dai, DataOutputQueue, setBlocking))
        .def("getBlocking", &DataOutputQueue::getBlocking, DOC(dai, DataOutputQueue, getBlocking))
        .def("setMaxSize", &DataOutputQueue::setMaxSize, py::arg("maxSize"), DOC(dai, DataOutputQueue, setMaxSize))
        .def("getMaxSize", &DataOutputQueue::getMaxSize, DOC(dai, DataOutputQueue, getMaxSize))
        .def("getAll", [](DataOutputQueue& obj){
          
            std::vector<std::shared_ptr<ADatatype>> messages;
            bool timedout = true;
            do {
                {          
                    // releases python GIL
                    py::gil_scoped_release release;

                    // block for 100ms
                    messages = obj.getAll(milliseconds(100), timedout);
                }

                // reacquires python GIL for PyErr_CheckSignals call

                // check if interrupt triggered in between
                if (PyErr_CheckSignals() != 0) throw py::error_already_set();

            } while(timedout); // Keep reiterating until a message is received (not timedout)

            return messages;
        }, DOC(dai, DataOutputQueue, getAll, 2))
        .def("get", [](DataOutputQueue& obj){
          
            std::shared_ptr<ADatatype> d = nullptr;
            bool timedout = true;
            do {
                {          
                    // releases python GIL
                    py::gil_scoped_release release;

                    // block for 100ms                    
                    d = obj.get(milliseconds(100), timedout);
                }

                // reacquires python GIL for PyErr_CheckSignals call

                // check if interrupt triggered in between
                if (PyErr_CheckSignals() != 0) throw py::error_already_set();

            } while(timedout);

            return d;
        }, DOC(dai, DataOutputQueue, get, 2))
        .def("has", static_cast<bool(DataOutputQueue::*)()>(&DataOutputQueue::has), DOC(dai, DataOutputQueue, has, 2))
        .def("tryGet", static_cast<std::shared_ptr<ADatatype>(DataOutputQueue::*)()>(&DataOutputQueue::tryGet), DOC(dai, DataOutputQueue, tryGet, 2))
        .def("tryGetAll", static_cast<std::vector<std::shared_ptr<ADatatype>>(DataOutputQueue::*)()>(&DataOutputQueue::tryGetAll), DOC(dai, DataOutputQueue, tryGetAll, 2))
        ;

    // Bind DataInputQueue
    py::class_<DataInputQueue, std::shared_ptr<DataInputQueue>>(m, "DataInputQueue", DOC(dai, DataInputQueue))
        .def("getName", &DataInputQueue::getName, DOC(dai, DataInputQueue, getName))
        .def("setBlocking", &DataInputQueue::setBlocking, py::arg("blocking"), DOC(dai, DataInputQueue, setBlocking))
        .def("getBlocking", &DataInputQueue::getBlocking, DOC(dai, DataInputQueue, getBlocking))
        .def("setMaxSize", &DataInputQueue::setMaxSize, py::arg("maxSize"), DOC(dai, DataInputQueue, setMaxSize))
        .def("getMaxSize", &DataInputQueue::getMaxSize, DOC(dai, DataInputQueue, getMaxSize))
        .def("send", [](DataInputQueue& obj, std::shared_ptr<ADatatype> d){
            
            bool sent = false;
            do {

                // block for 100ms
                {
                    // Release GIL, then block
                    py::gil_scoped_release release;
                    sent = obj.send(d, milliseconds(100));
                }

                // reacquires GIL as PyErr_CheckSignals requires GIL

                // check if interrupt triggered in between
                if (PyErr_CheckSignals() != 0) throw py::error_already_set();

            } while(!sent);

        }, py::arg("msg"), DOC(dai, DataInputQueue, send, 2))
        .def("send", [](DataInputQueue& obj, std::shared_ptr<dai::RawBuffer> d){

            bool sent = false;
            do {
                 // block for 100ms
                {
                    // Release GIL, then block
                    py::gil_scoped_release release;
                    sent = obj.send(d, milliseconds(100));
                }
                // reacquires GIL as PyErr_CheckSignals requires GIL

                // check if interrupt triggered in between
                if (PyErr_CheckSignals() != 0) throw py::error_already_set();

            } while(!sent);

        }, py::arg("rawMsg"), DOC(dai, DataInputQueue, send))
        ;

}