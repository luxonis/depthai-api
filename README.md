# DepthAI Python Library

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/pypi/v/depthai.svg)](https://pypi.org/project/depthai/)
[![Python Wheel CI](https://github.com/luxonis/depthai-python/actions/workflows/main.yml/badge.svg?branch=gen2_develop)](https://github.com/luxonis/depthai-python/actions/workflows/main.yml)

Python bindings for C++ depthai-core library

## Documentation

Documentation is available over at [Luxonis DepthAI API](https://docs.luxonis.com/projects/api/en/latest/)

### Building documentation

- **Using [Docker](https://docs.docker.com/) (with [Docker Compose](https://docs.docker.com/compose/install/))**

     ```
     cd docs
     docker-compose build
     docker-compose up
     ```
  
     Then open [http://localhost:8000](http://localhost:8000).
     
     This docker container will watch changes in the `docs/source` directory and rebuild the docs automatically

- **Linux**
     
     First, please install the required [dependencies](#Dependencies)
  
     Then run the following commands to build the docs website
  
     ```
     python3 -m pip install -U pip
     python3 -m pip install -r docs/requirements.txt
     cmake -S . -B build -D DEPTHAI_BUILD_DOCS=ON -D DEPTHAI_PYTHON_BUILD_DOCS=ON
     cmake --build build --target sphinx --parallel 8
     python3 -m http.server --bind 0.0.0.0 8000 --directory build/docs/sphinx
     ```
  
     Then open [http://localhost:8000](http://localhost:8000).

     This will build documentation based on current sources, so if some new changes will be made, run this command
     in a new terminal window to update the website source
  
     ```
     cmake --build build --target sphinx --parallel 8
     ```
  
     Then refresh your page - it should load the updated website that was just built
  

## Installation

Prebuilt wheels are available in [Luxonis repository](https://artifacts.luxonis.com/artifactory/luxonis-python-snapshot-local/)
Make sure pip is upgraded
```
python3 -m pip install -U pip
python3 -m pip install --extra-index-url https://artifacts.luxonis.com/artifactory/luxonis-python-snapshot-local/ depthai
```
## Building from source

### Dependencies
 - cmake >= 3.4
 - C++14 compiler (clang, gcc, msvc, ...)
 - Python

Along these, dependencies of depthai-core are also required
See: [depthai-core dependencies](https://github.com/luxonis/depthai-core#dependencies)


### Building

To build a shared library from source perform the following:
```
git submodule update --init --recursive
mkdir build && cd build
cmake .. [-D PYTHON_EXECUTABLE=/full/path/to/python]
cmake --build . --parallel 8
```

Where `-D PYTHON_EXECUTABLE` option can optionally specify an exact Python executable to use for building.

To build a wheel, execute the following
```
python3 -m pip wheel . -w wheelhouse
```

To build and install using pip:
```
python3 -m pip install .
```

## Running tests

To run the tests build the library with the following options
```
git submodule update --init --recursive
mkdir build_tests && cd build_tests
cmake .. -D DEPTHAI_PYTHON_ENABLE_TESTS=ON -D DEPTHAI_PYTHON_ENABLE_EXAMPLES=ON -D DEPTHAI_PYTHON_TEST_EXAMPLES=ON
cmake --build . --parallel 8
ctest
```


## Tested platforms

- Windows 10
- Ubuntu 16.04, 18.04;
- Raspbian 10;
- macOS 10.14.6, 10.15.4;

## Troubleshooting

### Relocation link error

Build failure on Ubuntu 18.04 ("relocation ..." link error) with gcc 7.4.0 (default) - [**issue #3**](https://github.com/luxonis/depthai-api/issues/3)
   - the solution was to upgrade gcc to version 8:

         sudo apt install g++-8
         sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 70
         sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-8 70
### Hunter
Hunter is a CMake-only dependency manager for C/C++ projects. 

If you are stuck with error message which mentions external libraries (subdirectory of `.hunter`) like the following:
```
/usr/bin/ld: /home/[user]/.hunter/_Base/062a19a/ccfed35/a84a713/Install/lib/liblzma.a(stream_flags_decoder.c.o): warning: relocation against `lzma_footer_magic' in read-only section `.text'
```

Try erasing the **Hunter** **cache** folder.

Linux/MacOS:
```
rm -r ~/.hunter
```
Windows:
```
del C:/.hunter
```
or
```
del C:/[user]/.hunter
```

### LTO - link time optimization

If following message appears: 
```
lto1: internal compiler error: in add_symbol_to_partition_1, at lto/lto-partition.c:152
Please submit a full bug report,
with preprocessed source if appropriate.
See <file:///usr/share/doc/gcc-10/README.Bugs> for instructions.
lto-wrapper: fatal error: /usr/bin/c++ returned 1 exit status
compilation terminated.
/usr/bin/ld: error: lto-wrapper failed
collect2: error: ld returned 1 exit status
make[2]: *** [CMakeFiles/depthai.dir/build.make:227: depthai.cpython-38-x86_64-linux-gnu.so] Error 1
make[1]: *** [CMakeFiles/Makefile2:98: CMakeFiles/depthai.dir/all] Error 2
make: *** [Makefile:130: all] Error 2
```

One fix is to update linker: (In case you are on Ubuntu 20.04: `/usr/bin/ld --version`: 2.30)
```
# Add to the end of /etc/apt/sources.list:

echo "deb http://ro.archive.ubuntu.com/ubuntu groovy main" >> /etc/apt/sources.list

# Replace ro with your countries local cache server (check the content of the file to find out which is)
# Not mandatory, but faster

sudo apt update
sudo apt install binutils

# Should upgrade to 2.35.1
# Check version:
/usr/bin/ld --version
# Output should be: GNU ld (GNU Binutils for Ubuntu) 2.35.1
# Revert /etc/apt/sources.list to previous state (comment out line) to prevent updating other packages.
sudo apt update
```

Another option is to use **clang** compiler:
```
sudo apt install clang-10
mkdir build && cd build
CC=clang-10 CXX=clang++-10 cmake ..
cmake --build . --parallel 8
```
