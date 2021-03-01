cmake_minimum_required(VERSION 3.4) # For Hunter

# Set defaults
# PIC toolchain as we are building a shared library
set(CMAKE_TOOLCHAIN_FILE "${CMAKE_CURRENT_LIST_DIR}/cmake/toolchain/pic.cmake" CACHE STRING "")

# Build dependencies as 'Release' only by default (if not MSVC, as it requires same debug level for libraries to be linked against)
if(NOT WIN32)
    set(HUNTER_CONFIGURATION_TYPES "Release" CACHE STRING "Hunter dependencies list of build configurations")
endif()

# Generate combined Hunter config
file(READ depthai-core/cmake/Hunter/config.cmake depthai_core_hunter_config)
file(READ cmake/Hunter/config.cmake hunter_config)
string(CONCAT final_hunter_config ${depthai_core_hunter_config} "\n\n" ${hunter_config})
file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/generated/Hunter/config.cmake ${final_hunter_config})

include("cmake/HunterGate.cmake")
HunterGate(
    URL "https://github.com/cpp-pm/hunter/archive/v0.23.258.tar.gz"
    SHA1 "062a19ab13ce8dffa9a882b6ce3e43bdabdf75d3"
    FILEPATH ${CMAKE_CURRENT_BINARY_DIR}/generated/Hunter/config.cmake # Combined config
)

# Move binary dir if windows, to shorten the path
if(WIN32)
    set(HUNTER_BINARY_DIR "${HUNTER_GATE_ROOT}/_bin" CACHE STRING "Hunter binary directory")
endif()

# Pybindings project
set(TARGET_NAME depthai)
project(depthai VERSION "0") # revision of bindings [depthai-core].[rev]

# Add module paths
list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake/")
list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/depthai-core/cmake")

# Constants
set(DOCSTRINGS_INCLUDE_PLACEHOLDER_DIR ${CMAKE_CURRENT_BINARY_DIR}/generated/include)
set(DOCSTRINGS_INCLUDE_PLACEHOLDER_PATH ${DOCSTRINGS_INCLUDE_PLACEHOLDER_DIR}/docstring.hpp)
set(DOCSTRINGS_OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/generated/include/depthai_python_docstring.hpp)

# First specify options
option(DEPTHAI_PYTHON_ENABLE_TESTS "Enable tests" OFF)
option(DEPTHAI_PYTHON_ENABLE_EXAMPLES "Enable examples" OFF)
option(DEPTHAI_PYTHON_BUILD_DOCS "Build documentation - see docs/requirements.txt for needed dependencies" OFF)
option(DEPTHAI_PYTHON_BUILD_DOCSTRINGS "Generate docstrings from header files if module 'pybind11_mkdoc' available" ON)
set(DEPTHAI_PYTHON_DOCSTRINGS_INPUT ${DOCSTRINGS_OUTPUT} CACHE FILEPATH "Path to docstring for bindings") 
set(DEPTHAI_PYTHON_DOCSTRINGS_OUTPUT ${DOCSTRINGS_OUTPUT} CACHE FILEPATH "Path where docstring file will be generated") 
if(DEPTHAI_PYTHON_BUILD_DOCSTRINGS)
    option(DEPTHAI_PYTHON_FORCE_DOCSTRINGS "Force that docstrings are generated, module 'pybind11_mkdoc' required" OFF)
endif()

# Add external dependencies
add_subdirectory(external)

# Add depthai-cpp dependency
add_subdirectory(depthai-core)

# Add pybind11 dependency
#add_subdirectory(pybind11-2.5.0)
hunter_add_package(pybind11)

# Disable LTO if MINGW compiler
if(MINGW)   
    set(PYBIND11_LTO_CXX_FLAGS "" CACHE STRING "" FORCE)
endif()
find_package(pybind11 CONFIG REQUIRED)

# Add files for python module
pybind11_add_module(${TARGET_NAME} 
    src/py_bindings.cpp
    src/XLinkConnectionBindings.cpp
    src/DeviceBindings.cpp
    src/DeviceBootloaderBindings.cpp
    src/DatatypeBindings.cpp
    src/DataQueueBindings.cpp
    src/pipeline/PipelineBindings.cpp
    src/pipeline/NodeBindings.cpp
    src/pipeline/CommonBindings.cpp
    src/pipeline/AssetManagerBindings.cpp
    src/openvino/OpenVINOBindings.cpp
    src/log/LogBindings.cpp
)

# Configure include placeholder with INPUT path
configure_file(cmake/docstring.hpp.in ${DOCSTRINGS_INCLUDE_PLACEHOLDER_PATH})
# Add target to generate docstrings
if (DEPTHAI_PYTHON_BUILD_DOCSTRINGS)
    include(pybind11-mkdoc)
    # Check if pybind11_mkdoc available and create target
    target_pybind11_mkdoc_setup(${DEPTHAI_PYTHON_DOCSTRINGS_OUTPUT} depthai-core ${DEPTHAI_PYTHON_FORCE_DOCSTRINGS})
    if(NOT TARGET pybind11_mkdoc)
        # Generate default docstrings to OUTPUT path
        configure_file(cmake/default_docstring.hpp.in ${DEPTHAI_PYTHON_DOCSTRINGS_OUTPUT} COPYONLY)
    endif()
else()
    # Generate default docstrings to OUTPUT path
    configure_file(cmake/default_docstring.hpp.in ${DEPTHAI_PYTHON_DOCSTRINGS_OUTPUT} COPYONLY)
endif()

# Add include directory
target_include_directories(${TARGET_NAME} PRIVATE src ${DOCSTRINGS_INCLUDE_PLACEHOLDER_DIR})

# Link with libraries
target_link_libraries(${TARGET_NAME} 
    PUBLIC 
        # pybind11
        pybind11::pybind11
        depthai::core # Use non-opencv target as we use opencv-python in bindings
        hedley
)

# Version consists of: (depthai-core).(bindings revision)[+bindings hash]
set(DEPTHAI_PYTHON_VERSION "${DEPTHAI_VERSION}.${PROJECT_VERSION}")

# Add default commit hash ('dev') if not build by CI
if(NOT DEFINED ENV{CI} AND NOT DEPTHAI_PYTHON_COMMIT_HASH)   
    set(DEPTHAI_PYTHON_COMMIT_HASH dev)
endif()

# Append build info to version
if(DEPTHAI_PYTHON_COMMIT_HASH)
    set(DEPTHAI_PYTHON_VERSION "${DEPTHAI_PYTHON_VERSION}+${DEPTHAI_PYTHON_COMMIT_HASH}")    
endif()

# Add version definition
target_compile_definitions(${TARGET_NAME} PRIVATE DEPTHAI_PYTHON_VERSION="${DEPTHAI_PYTHON_VERSION}")
target_compile_definitions(${TARGET_NAME} PRIVATE DEPTHAI_PYTHON_BINDINGS_REVISION="${PROJECT_VERSION}")
target_compile_definitions(${TARGET_NAME} PRIVATE DEPTHAI_VERSION="${DEPTHAI_VERSION}")
target_compile_definitions(${TARGET_NAME} PRIVATE DEPTHAI_PYTHON_COMMIT_HASH="${DEPTHAI_PYTHON_COMMIT_HASH}")

# Set compiler features (c++14), and disables extensions
set_property(TARGET ${TARGET_NAME} PROPERTY CXX_STANDARD 14)
set_property(TARGET ${TARGET_NAME} PROPERTY CXX_STANDARD_REQUIRED ON)
set_property(TARGET ${TARGET_NAME} PROPERTY CXX_EXTENSIONS OFF)

# ASAN Settings as we are building and using shared library
if(SANITIZE_ADDRESS OR SANITIZE_MEMORY OR SANITIZE_THREAD OR SANITIZE_UNDEFINED)
    # Get asan library to preload
    if (CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
        execute_process(COMMAND ${CMAKE_CXX_COMPILER} -print-file-name=libclang_rt.asan-${CMAKE_HOST_SYSTEM_PROCESSOR}.so OUTPUT_VARIABLE LIBASAN_PATH OUTPUT_STRIP_TRAILING_WHITESPACE)
    elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
        execute_process(COMMAND ${CMAKE_CXX_COMPILER} -print-file-name=libasan.so OUTPUT_VARIABLE LIBASAN_PATH OUTPUT_STRIP_TRAILING_WHITESPACE)
    endif()
    # Set preload env variable
    if(APPLE)
        set(ASAN_ENVIRONMENT_VARS "DYLD_INSERT_LIBRARIES=${LIBASAN_PATH}" "ASAN_OPTIONS=leak_check_at_exit=0")
    elseif(UNIX)
        set(ASAN_ENVIRONMENT_VARS "LD_PRELOAD=${LIBASAN_PATH}" "ASAN_OPTIONS=leak_check_at_exit=0")
    endif()
    message(STATUS "ASAN environment variables: ${ASAN_ENVIRONMENT_VARS}")
endif()

########################
# Testing
########################
if(DEPTHAI_PYTHON_ENABLE_TESTS OR DEPTHAI_PYTHON_ENABLE_EXAMPLES)
    include(CTest)
    enable_testing()
endif()

########################
# Tests
########################
if (DEPTHAI_PYTHON_ENABLE_TESTS)
    add_subdirectory(tests)
endif()

########################
# Examples (can also act as tests)
########################
if (DEPTHAI_PYTHON_ENABLE_EXAMPLES)
    add_subdirectory(examples)
endif()

########################
# Documentation
########################
if(DEPTHAI_PYTHON_BUILD_DOCS)
    add_subdirectory(docs)
endif()
