FROM python:3.9

RUN apt-get update && apt-get install -y cmake libusb-1.0-0-dev build-essential cmake unzip pkg-config libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran python3-dev
RUN pip install -U pip numpy

WORKDIR /libs
RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.5.1.zip && unzip opencv.zip && mv opencv-4.5.1 opencv
RUN wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.5.1.zip && unzip opencv_contrib.zip && mv opencv_contrib-4.5.1 opencv_contrib
WORKDIR /libs/opencv/build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_EXTRA_MODULES_PATH=/libs/opencv_contrib/modules \
    -D BUILD_EXAMPLES=ON .. && \
    make -j 8 && \
    make install


WORKDIR /app
ADD docs/requirements.txt docs/requirements.txt
RUN pip install -r docs/requirements.txt
ADD . .
CMD docs/docker_run.sh