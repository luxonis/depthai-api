FROM luxonis/depthai-base:latest

RUN apt install wget
RUN wget https://github.com/libusb/libusb/releases/download/v1.0.24/libusb-1.0.24.tar.bz2
RUN tar xf libusb-1.0.24.tar.bz2
RUN cd libusb-1.0.24 && \
    ./configure --disable-udev && \
    make -j && make install

RUN pip install opencv-python

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
