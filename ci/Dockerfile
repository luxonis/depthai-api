FROM python:3.7-buster

RUN apt-get update && apt-get install -y wget build-essential cmake pkg-config libjpeg-dev libtiff5-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran
RUN wget http://docs.luxonis.com/_static/install_dependencies.sh && chmod +x install_dependencies.sh && ./install_dependencies.sh
RUN wget https://github.com/libusb/libusb/releases/download/v1.0.24/libusb-1.0.24.tar.bz2
RUN tar xf libusb-1.0.24.tar.bz2
RUN cd libusb-1.0.24 && \
    ./configure --disable-udev && \
    make -j && make install


RUN pip install --extra-index-url https://www.piwheels.org/simple/ opencv-python

COPY . /depthai-python
RUN mkdir -p depthai-python/build
RUN cd /depthai-python && \
    cd build && \
    cmake .. && \
    make -j
ENV PYTHONPATH=/depthai-python/build

RUN mkdir -p /depthai-python/examples/models/
RUN cd /depthai-python/examples/models/ && \
    wget https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/mobilenet-ssd_openvino_2021.2_6shave.blob
