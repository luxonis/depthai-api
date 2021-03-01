#pragma once

// pybind
#include "pybind11_common.hpp"

struct CommonBindings {
    static void bind(pybind11::module& m);
};
