# Copyright (c) 2020, Riverbank Computing Limited
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import argparse
import os
import shutil
import subprocess
import sys
#import time
#import utils.pdt_parser as pdtp
#from datetime import datetime


def run(args):
    """ Run a command and terminate if it fails. """

    try:
        ec = subprocess.call(' '.join(args), shell=True)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
        ec = 1

    if ec:
        sys.exit(ec)


# Initialise handy variables and tools
## Define current script location as reference
build_script_dir = os.path.dirname(os.path.realpath(__file__))
## Define default variable values
app_name_default = "MyCrossPlatformApp"
app_release_dir_default = build_script_dir
## Instantiate pdt_parser object
### TODO
## Get essential information from pdt file
### TODO
## Generate practical release directory structure
### TODO

# Parse the command line.
parser = argparse.ArgumentParser()
parser.add_argument('--jobs',
        help="the number of make jobs to be run in parallel on Linux and "
                "macOS [default: 1]",
        metavar="NUMBER", type=int, default=1)
parser.add_argument('--pdt',
        help="the pdt file used to define app sources and imported packages",
        metavar="FILE")      
parser.add_argument('--qmake',
        help="the qmake executable when using an existing Qt installation",
        metavar="FILE")
parser.add_argument('--target', help="the target architecture", default='')
parser.add_argument('--quiet', help="disable progress messages",
        action='store_true')
parser.add_argument('--verbose', help="enable verbose progress messages",
        action='store_true')
cmd_line_args = parser.parse_args()
jobs = cmd_line_args.jobs
qmake = os.path.abspath(cmd_line_args.qmake) if cmd_line_args.qmake else None
target = cmd_line_args.target
quiet = cmd_line_args.quiet
verbose = cmd_line_args.verbose

# Pick a default target if none is specified.
if not target:
    if sys.platform == 'win32':
        # MSVC2015 is v14, MSVC2017 is v15, MSVC2019 is v16.
        vs_major = os.environ.get('VisualStudioVersion', '0.0').split('.')[0]

        if vs_major == '0':
            # If there is no development environment then use the host
            # platform.
            from distutils.util import get_platform

            is_32 = (get_platform() == 'win32')
        elif vs_major == '14':
            is_32 = (os.environ.get('Platform') != 'X64')
        else:
            is_32 = (os.environ.get('VSCMD_ARG_TGT_ARCH') != 'x64')

        target = 'win-' + ('32' if is_32 else '64')
    elif sys.platform == 'darwin':
        target = 'macos-64'
    elif sys.platform.startswith('linux'):
        import struct

        target = 'linux-{0}'.format(8 * struct.calcsize('P'))
    else:
        print("Unsupported platform:", sys.platform, file=sys.stderr)
        sys.exit(2)

# Make sure qmake was specified only if it is needed.
if target in ('android-32', 'android-64', 'ios-64'):
    if not qmake:
        print("--qmake must be specified for", target, file=sys.stderr)
        sys.exit(2)
else:
    if qmake:
        print("--qmake must not be specified for", target, file=sys.stderr)
        sys.exit(2)

# Anchor everything from the directory containing this script.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Build the sysroot.  This won't do anything if it is already built.
args = ['pyqtdeploy-sysroot', '--target', target]

if jobs > 1:
    args.append('--jobs')
    args.append(str(jobs))

if qmake:
    args.append('--qmake')
    args.append(qmake)

if quiet:
    args.append('--quiet')

if verbose:
    args.append('--verbose')

args.append('sysroot.toml')

run(args)

# Build the demo.
build_dir = 'build-' + target

# shutil.copy('pyqt-demo.py', os.path.join('data', 'pyqt-demo.py.dat'))

args = ['pyqtdeploy-build', '--target', target, '--build-dir', build_dir]

if qmake:
    args.append('--qmake')
    args.append(qmake)

if quiet:
    args.append('--quiet')

if verbose:
    args.append('--verbose')

args.append('pyqt-demo.pdt')

run(args)

# Run qmake.  Use the qmake left by pyqtdeploy-sysroot if there is one.
sysroot_dir = os.path.abspath('sysroot-' + target)
qmake_path = os.path.join(sysroot_dir, 'Qt', 'bin', 'qmake')

if sys.platform == 'win32':
    qmake_path += '.exe'

if not os.path.isfile(qmake_path):
    qmake_path = qmake

os.chdir(build_dir)
run([qmake_path])

# Run make. (When targeting iOS we leave it to Xcode.)
if target.startswith('ios'):
    pass
else:
    # We only support MSVC on Windows.
    make = 'nmake' if sys.platform == 'win32' else 'make'

    run([make])

    if target.startswith('android'):
        if os.path.isfile('android-CrossPlatformDemoApp-deployment-settings.json'):
            # Qt v5.14 or later.
            run([make, 'apk'])
            apk = 'CrossPlatformDemoApp.apk'
            apk_dir = os.path.join(build_dir, 'android-build')
        else:
            # Qt v5.13 or earlier.
            run([make, 'INSTALL_ROOT=' + 'pyqt-demo', 'install'])
            run([os.path.join(os.path.dirname(qmake_path), 'androiddeployqt'),
                    '--gradle', '--input',
                    'android-libpyqt-demo.so-deployment-settings.json',
                    '--output', 'pyqt-demo'])
            apk = 'pyqt-demo-debug.apk'
            apk_dir = os.path.join(build_dir, 'pyqt-demo', 'build', 'outputs',
                    'apk', 'debug')

# Tell the user where the demo is.
if target.startswith('android'):
    print("""The {0} file can be found in the '{1}'
directory.  Run adb to install it to a simulator.""".format(apk, apk_dir))

elif target.startswith('ios'):
    print("""The pyqt-demo.xcodeproj file can be found in the '{0}' directory.
Run Xcode to build the app and run it in the simulator or deploy it to a
device.""".format(build_dir))

elif target.startswith('win') or sys.platform == 'win32':
    print("The pyqt-demo executable can be found in the '{0}' directory.".format(os.path.join(build_dir, 'release')))

else:
    print("The pyqt-demo executable can be found in the '{0}' directory.".format(build_dir))
