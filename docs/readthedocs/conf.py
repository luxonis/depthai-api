# readthedocs CI build limitation circumvent
import subprocess
import os
import sys

# Get current working directory
cwd = os.path.dirname(os.path.realpath(__file__))

# Prepare dependencies for library
env=os.environ.copy()

# Temp dir - remove if exists, and create a new one
tmpdir = '/home/docs/__temp_dir/'
subprocess.check_call(['rm', '-rf', tmpdir])
subprocess.check_call(['mkdir', '-p', tmpdir])

# Libusb
subprocess.check_call(['wget', 'https://github.com/libusb/libusb/releases/download/v1.0.24/libusb-1.0.24.tar.bz2'], cwd=tmpdir)
subprocess.check_call(['tar', 'xf', 'libusb-1.0.24.tar.bz2'], cwd=tmpdir)
subprocess.check_call(['./configure', '--disable-udev', '--prefix', tmpdir+'/libusb'], cwd=tmpdir+'/libusb-1.0.24')
subprocess.check_call(['make', '-j'], cwd=tmpdir+'/libusb-1.0.24')
subprocess.check_call(['make', 'install'], cwd=tmpdir+'/libusb-1.0.24')
env['PATH'] = tmpdir+'/libusb/include:'+tmpdir+'/libusb/lib'+':'+env['PATH']

# libclang
subprocess.check_call(['wget', 'https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/misc/libclang-11_manylinux2014_x86_64.tar.xz'], cwd=tmpdir)
subprocess.check_call(['mkdir', '-p', 'libclang'], cwd=tmpdir)
subprocess.check_call(['tar', 'xf', 'libclang-11_manylinux2014_x86_64.tar.xz', '-C', tmpdir+'/libclang/'], cwd=tmpdir)
env['LIBCLANG_PATH'] = tmpdir+'/libclang/usr/lib/llvm-11/lib/libclang.so.1'
env['LLVM_DIR_PATH'] = tmpdir+'/libclang/usr/lib/llvm-11/'

# Build library and generate actual conf.py
subprocess.run(["cmake -P ci.cmake"], cwd=cwd, shell=True, check=True, env=env)

# Load generated conf.py which includes all needed information to build with sphinx
with open("../../build/docs/conf.py") as infile:
    exec(infile.read())
