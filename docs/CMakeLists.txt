# This list specifies building of documentation using CMake

# Specify path separator
set(SYS_PATH_SEPARATOR ";")
if(UNIX)
    set(SYS_PATH_SEPARATOR ":")
endif()

# Get doxygen build location form doxygen target
get_target_property(DOXYGEN_OUTPUT_DIR doxygen DOXYGEN_OUTPUT_DIR)
message(STATUS "Retrieved doxygen output dir from doxygen target: ${DOXYGEN_OUTPUT_DIR}")

# Add year information
string(TIMESTAMP build_year "%Y")
# Configure sphinx for the build
configure_file(conf.py.in "${CMAKE_CURRENT_BINARY_DIR}/conf.py" @ONLY)

# Sphinx is required to build python documentation
# Find Python sphinx, by checking python -m sphinx
message(STATUS "Checking for sphinx")
execute_process(COMMAND ${PYTHON_EXECUTABLE} -m sphinx --version RESULT_VARIABLE error OUTPUT_QUIET ERROR_QUIET)
if(error)
    set(message "Checking for sphinx - not found, target 'sphinx' not available")
    if(NOT enforce)
        message(STATUS ${message})
    else()
        message(FATAL_ERROR ${message})
    endif()
    # Exit
    return()
else()
    message(STATUS "Checking for sphinx - found, target 'sphinx' available")

    # Set input and output
    set(SPHINX_SOURCE ${CMAKE_CURRENT_LIST_DIR}/source)
    set(SPHINX_BUILD ${CMAKE_CURRENT_BINARY_DIR}/sphinx)

    # Ready up sphinx - needed values configured in conf.py
    add_custom_target(sphinx ALL
        ${CMAKE_COMMAND} -E env 
        # Environment variables
        # Python path (to find compiled module)
        "PYTHONPATH=$<TARGET_FILE_DIR:${TARGET_NAME}>${SYS_PATH_SEPARATOR}$ENV{PYTHONPATH}"
        # ASAN in case of sanitizers
        "${ASAN_ENVIRONMENT_VARS}" 
        ############ SPHINX
        ${PYTHON_EXECUTABLE} -m sphinx -c ${CMAKE_CURRENT_BINARY_DIR} -b html ${SPHINX_SOURCE} ${SPHINX_BUILD}
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Generating documentation with Sphinx"
        VERBATIM
        COMMAND_EXPAND_LISTS
    )

    # Add dependency to library
    add_dependencies(sphinx ${TARGET_NAME})

endif()