import os
import re
import sys
import platform
import subprocess
import find_version

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.2.0':
                raise RuntimeError("CMake >= 3.2.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):

        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        # required for auto-detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        # Memcheck (guard if it fails)
        totalMemory = 4000
        if platform.system() == "Linux":
            try:
                totalMemory = int(os.popen("free -m").readlines()[1].split()[1])
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                totalMemory = 4000

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            cmake_args += ['-DCMAKE_TOOLCHAIN_FILE={}'.format(os.path.dirname(os.path.abspath(__file__)) + '/ci/msvc_toolchain.cmake')]
            
            # Detect whether 32 / 64 bit Python is used and compile accordingly
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            # if macos
            if sys.platform == 'darwin':
                from distutils import util
                os.environ['MACOSX_DEPLOYMENT_TARGET'] = '10.9'
                os.environ['_PYTHON_HOST_PLATFORM'] = re.sub(r'macosx-[0-9]+\.[0-9]+-(.+)', r'macosx-10.9-\1', util.get_platform())

            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
           
            #Memcheck
            parallel_args = ['--', '-j']
            if totalMemory < 1000:
                parallel_args = ['--', '-j1']
                cmake_args += ['-DHUNTER_JOBS_NUMBER=1']
            elif totalMemory < 2000:
                parallel_args = ['--', '-j2']
                cmake_args += ['-DHUNTER_JOBS_NUMBER=2']
            build_args += parallel_args

        # Hunter configuration to release only
        cmake_args += ['-DHUNTER_CONFIGURATION_TYPES=Release']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''), self.distribution.get_version())
        
        # Add additional cmake args
        if 'CMAKE_ARGS' in os.environ:
            cmake_args += [os.environ['CMAKE_ARGS']]

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)


### GENERATED VERSION - Do not modify
final_version = find_version.get_package_version()
if 'BUILD_COMMIT_HASH' in os.environ:
    final_version = final_version + '+' + os.environ['BUILD_COMMIT_HASH']

setup(
    name='depthai',
    version=final_version,
    author='Martin Peterlin',
    author_email='martin@luxonis.com',
    description='DepthAI Python Library',
    long_description='',
    ext_modules=[CMakeExtension('depthai')],
    cmdclass={
        'build_ext': CMakeBuild
    },
    zip_safe=False,
)
