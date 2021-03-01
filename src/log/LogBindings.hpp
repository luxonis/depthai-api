#pragma once

// pybind
#include "pybind11_common.hpp"

struct LogBindings {
    static void bind(pybind11::module& m);
};
