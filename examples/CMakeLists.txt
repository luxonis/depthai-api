# Prevent from being configured
if(CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
    message(FATAL_ERROR "Use projects root CMakeLists.txt to configure")
endif()

# Add options
option(DEPTHAI_PYTHON_TEST_EXAMPLES "Test examples - examples will be ran as a part of the test suite" OFF)

# Specify path separator
set(SYS_PATH_SEPARATOR ";")
if(UNIX)
    set(SYS_PATH_SEPARATOR ":")
endif()

# Add a target to install_requirements (added to ALL)
add_custom_target(install_requirements ALL
    COMMAND ${PYTHON_EXECUTABLE} "${CMAKE_CURRENT_LIST_DIR}/install_requirements.py" "--skip_depthai"
    DEPENDS ${TARGET_NAME}
    VERBATIM
    COMMAND_EXPAND_LISTS
)

# Macro for adding new python test
macro(add_python_example example_name python_script_path)
    # parse the rest of the arguments
    set(arguments ${ARGV})
    list(REMOVE_AT arguments 0 1)

    # Creates a target (python my_test [args])
    add_custom_target(${example_name}
        ${CMAKE_COMMAND} -E env
        # Environment variables
        # Python path (to find compiled module)
        "PYTHONPATH=$<TARGET_FILE_DIR:${TARGET_NAME}>${SYS_PATH_SEPARATOR}$ENV{PYTHONPATH}"
        # ASAN in case of sanitizers
        "${ASAN_ENVIRONMENT_VARS}"
        # Example
        ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/${python_script_path} ${ARGN}
        DEPENDS ${TARGET_NAME} install_requirements
        VERBATIM
        COMMAND_EXPAND_LISTS
    )

    if(DEPTHAI_PYTHON_TEST_EXAMPLES)

        # Adds test with 5 seconds timeout and bumps all python warnings to errors
        add_test(NAME ${example_name} COMMAND
            ${CMAKE_COMMAND} -E env
            # Python path (to find compiled module)
            "PYTHONPATH=$<TARGET_FILE_DIR:${TARGET_NAME}>${SYS_PATH_SEPARATOR}$ENV{PYTHONPATH}"
            # ASAN in case of sanitizers
            ${ASAN_ENVIRONMENT_VARS}
            ${CMAKE_COMMAND} -DTIMEOUT_SECONDS=5 -P ${CMAKE_CURRENT_LIST_DIR}/cmake/ExecuteTestTimeout.cmake
            # Actual script to run
            ${PYTHON_EXECUTABLE} -Werror "${CMAKE_CURRENT_LIST_DIR}/${python_script_path}" ${arguments}
        )

        # Sets a regex catching any logged warnings, errors or critical (coming either from device or host)
        set_tests_properties (${example_name} PROPERTIES FAIL_REGULAR_EXPRESSION "\\[warning\\];\\[error\\];\\[critical\\]")

    endif()

endmacro()

if(DEPTHAI_PYTHON_TEST_EXAMPLES)

    # Adds install requirements test with 5 minute timeout
    add_test(NAME install_requirements COMMAND
        ${CMAKE_COMMAND} -E env
        # Python path (to find compiled module)
        "PYTHONPATH=$<TARGET_FILE_DIR:${TARGET_NAME}>${SYS_PATH_SEPARATOR}$ENV{PYTHONPATH}"
        # ASAN in case of sanitizers
        ${ASAN_ENVIRONMENT_VARS}
        ${CMAKE_COMMAND} -DFORCE_TIMEOUT_SECONDS=300 -P ${CMAKE_CURRENT_LIST_DIR}/cmake/ExecuteTestTimeout.cmake
        # Actual script to run
        ${PYTHON_EXECUTABLE} "${CMAKE_CURRENT_LIST_DIR}/install_requirements.py" "--skip_depthai"
    )

    # Sets a regex catching any logged warnings, errors or critical (coming either from device or host)
    set_tests_properties (install_requirements PROPERTIES FAIL_REGULAR_EXPRESSION "\\[warning\\];\\[error\\];\\[critical\\]")

endif()

# Add examples
add_python_example(01_rgb_preview 01_rgb_preview.py)
add_python_example(02_mono_preview 02_mono_preview.py)
add_python_example(03_depth_preview 03_depth_preview.py)
add_python_example(04_rgb_encoding 04_rgb_encoding.py)
add_python_example(05_rgb_mono_encoding 05_rgb_mono_encoding.py)
add_python_example(06_rgb_full_resolution_saver 06_rgb_full_resolution_saver.py)
add_python_example(07_mono_full_resolution_saver 07_mono_full_resolution_saver.py)
add_python_example(08_rgb_mobilenet 08_rgb_mobilenet.py)
add_python_example(09_mono_mobilenet 09_mono_mobilenet.py)
add_python_example(10_mono_depth_mobilenetssd 10_mono_depth_mobilenetssd.py)
add_python_example(11_rgb_encoding_mono_mobilenet 11_rgb_encoding_mono_mobilenet.py)
add_python_example(12_rgb_encoding_mono_mobilenet_depth 12_rgb_encoding_mono_mobilenet_depth.py)
add_python_example(13_encoding_max_limit 13_encoding_max_limit.py)
add_python_example(14_1_color_camera_control 14_1_color_camera_control.py)
add_python_example(14_2_mono_camera_control 14_2_mono_camera_control.py)
add_python_example(14_3_depth_crop_control 14_3_depth_crop_control.py)
add_python_example(15_rgb_mobilenet_4k 15_rgb_mobilenet_4k.py)
add_python_example(16_device_queue_event 16_device_queue_event.py)
add_python_example(17_video_mobilenet 17_video_mobilenet.py)
add_python_example(18_rgb_encoding_mobilenet 18_rgb_encoding_mobilenet.py)
add_python_example(19_mono_camera_control 19_mono_camera_control.py)
add_python_example(20_color_rotate_warp 20_color_rotate_warp.py)
add_python_example(21_mobilenet_device_side_decoding 21_mobilenet_device_side_decoding.py)
add_python_example(22_1_tiny_yolo_v3_device_side_decoding 22_1_tiny_yolo_v3_device_side_decoding.py)
add_python_example(22_2_tiny_yolo_v4_device_side_decoding 22_2_tiny_yolo_v4_device_side_decoding.py)
add_python_example(23_autoexposure_roi 23_autoexposure_roi.py)
add_python_example(24_opencv_support 24_opencv_support.py)
add_python_example(25_system_information 25_system_information.py)
add_python_example(26_1_spatial_mobilenet 26_1_spatial_mobilenet.py)
add_python_example(26_2_spatial_mobilenet_mono 26_2_spatial_mobilenet_mono.py)
add_python_example(26_3_spatial_tiny_yolo_v3 26_3_spatial_tiny_yolo.py)
add_python_example(26_3_spatial_tiny_yolo_v4 26_3_spatial_tiny_yolo.py)
add_python_example(27_spatial_location_calculator 27_spatial_location_calculator.py)
add_python_example(28_camera_video_example 28_camera_video_example.py)
add_python_example(29_1_object_tracker 29_1_object_tracker.py)
add_python_example(29_2_spatial_object_tracker 29_2_spatial_object_tracker.py)
add_python_example(29_3_object_tracker_video 29_3_object_tracker_video.py)
add_python_example(30_stereo_depth_from_host 30_stereo_depth_from_host.py)
