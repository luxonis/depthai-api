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
        DEPENDS ${TARGET_NAME}
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

# Mobilenet resource
hunter_private_data(
    URL "https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/mobilenet-ssd_openvino_2021.2_6shave.blob"
    SHA1 "f0e14978b3f77a4f93b9f969cd39e58bb7aef490"
    FILE "mobilenet-ssd_openvino_2021.2_6shave.blob"
    LOCATION mobilenet_blob
)

# Mobilenet resource
hunter_private_data(
    URL "https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/mobilenet-ssd_openvino_2021.2_5shave.blob"
    SHA1 "d715f85e474609cf3f696d7a2e3750804ed6c726"
    FILE "mobilenet-ssd_openvino_2021.2_5shave.blob"
    LOCATION mobilenet_5shave_blob
)

# Construction vest video resource
hunter_private_data(
    URL "http://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/construction_vest.mp4"
    SHA1 "271d8d0b702e683ce02957db7c100843de5ceaec"
    FILE "construction_vest.mp4"
    LOCATION construction_vest
)

# tiny-yolo neural network resource
hunter_private_data(
    URL "https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/tiny-yolo-v3_openvino_2021.2_6shave.blob"
    SHA1 "f0ac263a0d55c374e1892eea21c9b7d1170bde46"
    FILE "tiny-yolo-v3_openvino_2021.2_6shave.blob"
    LOCATION tiny_yolo_v3_blob
)


# Add examples
add_python_example(01_rgb_preview 01_rgb_preview.py)
add_python_example(02_mono_preview 02_mono_preview.py)
add_python_example(03_depth_preview 03_depth_preview.py)
add_python_example(04_rgb_encoding 04_rgb_encoding.py)
add_python_example(05_rgb_mono_encoding 05_rgb_mono_encoding.py)
add_python_example(06_rgb_full_resolution_saver 06_rgb_full_resolution_saver.py)
add_python_example(07_mono_full_resolution_saver 07_mono_full_resolution_saver.py)
add_python_example(08_rgb_mobilenet 08_rgb_mobilenet.py "${mobilenet_blob}")
add_python_example(09_mono_mobilenet 09_mono_mobilenet.py "${mobilenet_blob}")
add_python_example(10_mono_depth_mobilenetssd 10_mono_depth_mobilenetssd.py "${mobilenet_blob}")
add_python_example(11_rgb_encoding_mono_mobilenet 11_rgb_encoding_mono_mobilenet.py "${mobilenet_blob}")
add_python_example(12_rgb_encoding_mono_mobilenet_depth 12_rgb_encoding_mono_mobilenet_depth.py "${mobilenet_blob}")
add_python_example(13_encoding_max_limit 13_encoding_max_limit.py)
add_python_example(14_color_camera_control 14_color_camera_control.py)
add_python_example(15_rgb_mobilenet_4k 15_rgb_mobilenet_4k.py "${mobilenet_5shave_blob}")
add_python_example(16_device_queue_event 16_device_queue_event.py)
add_python_example(17_video_mobilenet 17_video_mobilenet.py "${mobilenet_blob}" "${construction_vest}")
add_python_example(18_rgb_encoding_mobilenet 18_rgb_encoding_mobilenet.py "${mobilenet_blob}")
add_python_example(19_mono_camera_control 19_mono_camera_control.py)
add_python_example(20_color_rotate_warp 20_color_rotate_warp.py)
add_python_example(21_mobilenet_device_side_decoding 21_mobilenet_device_side_decoding.py "${mobilenet_blob}")
add_python_example(22_tiny_yolo_v3_device_side_decoding 22_tiny_yolo_v3_device_side_decoding.py "${tiny_yolo_v3_blob}")
add_python_example(23_autoexposure_roi 23_autoexposure_roi.py "${mobilenet_blob}")
add_python_example(24_opencv_support 24_opencv_support.py)
add_python_example(25_system_information 25_system_information.py)
