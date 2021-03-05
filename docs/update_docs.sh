#!/bin/bash

set -e

rm -rf build
cmake -S . -B build -D DEPTHAI_BUILD_DOCS=ON -D DEPTHAI_PYTHON_BUILD_DOCS=ON
cmake --build build --parallel --target sphinx