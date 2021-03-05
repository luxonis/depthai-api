FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y libusb-1.0-0-dev clang python3-opencv python3-pip clang-11 doxygen cmake git
RUN python3 -m pip install -U pip numpy

WORKDIR /app
ADD docs/requirements.txt docs/requirements.txt
RUN python3 -m pip install -r docs/requirements.txt
ADD . .
RUN cmake -S . -B build -D DEPTHAI_BUILD_DOCS=ON -D DEPTHAI_PYTHON_BUILD_DOCS=ON
RUN cmake --build build --parallel --target sphinx
CMD docs/docker_run.sh