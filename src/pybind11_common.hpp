#pragma once

#if (_MSC_VER >= 1910) || !defined(_MSC_VER) 
    #define HAVE_SNPRINTF
#endif

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <cstdint>

// Include docstring file
#include "docstring.hpp"

// Opaque types
//PYBIND11_MAKE_OPAQUE(std::vector<std::uint8_t>);


#include "tl/optional.hpp"
//using tl::optional;
namespace pybind11 { namespace detail {
    template <typename T>
    struct type_caster<tl::optional<T>> : optional_caster<tl::optional<T>> {};
}}

namespace py = pybind11;


