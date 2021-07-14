#!/bin/bash
set -e -x

# Install a system package required by our library
#yum install -y atlas-devel
yum install -y libusb1-devel
#yum remove -y libusb1

# Compile wheels
for PYBIN in /opt/python/cp3{6..9}*/bin; do
    #"${PYBIN}/pip" install -r /io/requirements.txt
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" --plat $PLAT -w /io/wheelhouse/ \
        || echo "Skipping non-platform wheel $whl"
done

# Install packages and test
#for PYBIN in /opt/python/*/bin/; do
#    "${PYBIN}/pip" install python-manylinux-demo --no-index -f /io/wheelhouse
#    (cd "$HOME"; "${PYBIN}/nosetests" pymanylinuxdemo)
#done
