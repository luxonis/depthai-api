# Depthai-Python examples

In this directory there are usage examples of depthai-python repository. 

## Setup

Navigate to root of repository and build Python module with DEPTHAI_PYTHON_TEST_EXAMPLES option enabled

```
mkdir -p build && cd build
cmake .. -DDEPTHAI_PYTHON_ENABLE_EXAMPLES=ON
cmake --build . --parallel 8
```

If you'd like to use a different Python interpreter, set `PYTHON_EXECUTABLE` to your interpreter location

```
cmake .. -DDEPTHAI_PYTHON_ENABLE_EXAMPLES=ON -D PYTHON_EXECUTABLE=/path/to/python
```

## Usage

To test all examples
```
ctest
```

To execute a specific example (without timeout)
```
TEST_TIMEOUT=0 ctest -R "01_rgb_preview" --verbose
```

## Demo

### 01_rgb_preview.py
![example_1](https://user-images.githubusercontent.com/5244214/104040973-9afd2800-51d8-11eb-8fe6-52649069ded5.gif)

### 02_mono_preview.py
![example_2](https://user-images.githubusercontent.com/5244214/104040960-959fdd80-51d8-11eb-8bde-fd706b5c8670.gif)

### 03_depth_preview.py

**NOTE** For clearness, a `disparity` output is used instead of `depth`, as disparity is better to visualize

![example_3](https://user-images.githubusercontent.com/5244214/104055993-fdadee00-51ef-11eb-9c52-882e1b0e734b.gif)

### 04_rgb_encoding.py
![example_4](https://user-images.githubusercontent.com/5244214/104040930-8f116600-51d8-11eb-888a-88272c34aed4.gif)

### 05_rgb_mono_encoding.py
![example_5](https://user-images.githubusercontent.com/5244214/104040921-8d47a280-51d8-11eb-9bc1-d809ec6cd9f6.gif)

### 06_rgb_full_resolution_saver.py
![example_6](https://user-images.githubusercontent.com/5244214/104040908-8882ee80-51d8-11eb-8817-1c8dca320f2b.gif)

### 07_mono_full_resolution_saver.py
![example_7](https://user-images.githubusercontent.com/5244214/104040905-86209480-51d8-11eb-9e15-5fe94aba7b69.gif)

### 08_rgb_mobilenet.py
![example_8](https://user-images.githubusercontent.com/5244214/112838840-cb4cb800-909d-11eb-8264-83d3c1e5f348.gif)

### 09_mono_mobilenet.py
![example_9](https://user-images.githubusercontent.com/5244214/112838832-ca1b8b00-909d-11eb-8ea1-eafeb98c3266.gif)

### 10_mono_depth_mobilenetssd.py

**NOTE** For clearness, a `disparity` output is used instead of `depth`, as disparity is better to visualize

![example_10](https://user-images.githubusercontent.com/5244214/112838828-c8ea5e00-909d-11eb-912a-ce3995a68bfd.gif)

### 11_rgb_encoding_mono_mobilenet.py
![example_11](https://user-images.githubusercontent.com/5244214/112838821-c851c780-909d-11eb-86d4-d7a6b6d0aebe.gif)

### 12_rgb_encoding_mono_mobilenet_depth.py

**NOTE** For clearness, a `disparity` output is used instead of `depth`, as disparity is better to visualize

![example_12](https://user-images.githubusercontent.com/5244214/112838818-c7209a80-909d-11eb-8f50-81c023c59e9b.gif)

### 13_encoding_max_limit.py
![example_13](https://user-images.githubusercontent.com/5244214/104741072-0307bd00-5749-11eb-97f3-9422c8b0d8da.gif)

### 14_color_camera_control.py
![example_14](https://user-images.githubusercontent.com/5244214/104741150-187ce700-5749-11eb-8bd5-3d4f37d2d22a.gif)

### 15_rgb_mobilenet_4k.py
![15](https://user-images.githubusercontent.com/5244214/112838812-c556d700-909d-11eb-8194-83602530c9af.gif)

### 16_device_queue_event.py
![16](https://user-images.githubusercontent.com/5244214/112838810-c425aa00-909d-11eb-9962-550533f13268.gif)

### 17_video_mobilenet.py
![17](https://user-images.githubusercontent.com/5244214/112838807-c38d1380-909d-11eb-9c89-878eaa20e4ed.gif)

### 18_rgb_encoding_mobilenet.py
![18](https://user-images.githubusercontent.com/5244214/112838805-c25be680-909d-11eb-8db2-2d0ce61aebe0.gif)

### 22_1_tiny_yolo_v3_device_side_decoding.py
![22_1](https://user-images.githubusercontent.com/5244214/112838798-c12ab980-909d-11eb-8e6c-5aa3d623c7e9.gif)

### 22_2_tiny_yolo_v4_device_side_decoding.py
![22_2](https://user-images.githubusercontent.com/5244214/112838790-bff98c80-909d-11eb-8b85-7c4dbd9a0e62.gif)

### 23_autoexposure_roi.py
![23](https://user-images.githubusercontent.com/5244214/112838784-be2fc900-909d-11eb-8067-291636ae9950.gif)

### 24_opencv_support.py
![24](https://user-images.githubusercontent.com/5244214/112838789-bf60f600-909d-11eb-9fb5-203dbec774f8.gif)

### 26_1_spatial_mobilenet.py
![26_1](https://user-images.githubusercontent.com/5244214/112838781-bcfe9c00-909d-11eb-9d12-a9834f545271.gif)

### 26_2_spatial_mobilenet_mono.py
![26_2](https://user-images.githubusercontent.com/5244214/112838777-bbcd6f00-909d-11eb-9b1e-d93159c3d88f.gif)

### 26_3_spatial_tiny_yolo.py
![26_3](https://user-images.githubusercontent.com/5244214/112838772-ba9c4200-909d-11eb-9678-0703df46b529.gif)

### 28_camera_video_example.py
![28](https://user-images.githubusercontent.com/5244214/112838767-b8d27e80-909d-11eb-92f0-5af20c4326b7.gif)

