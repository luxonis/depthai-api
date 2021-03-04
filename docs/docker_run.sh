#!/bin/bash

set -e

apt-get install -y doxygen python3-dev
rm -rf build
cmake -S . -B build -D DEPTHAI_BUILD_DOCS=ON -D DEPTHAI_PYTHON_BUILD_DOCS=ON
cmake --build build --parallel --target sphinx
python -m http.server 0.0.0.0:8000