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
import time
import resources.python.pdt_parser as pdtp
from datetime import datetime


def run(args):
    """ Run a command and terminate if it fails. """

    try:
        ec = subprocess.call(' '.join(args), shell=True)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
        ec = 1

    if ec:
        sys.exit(ec)


# Parse the command line.
parser = argparse.ArgumentParser()
parser.add_argument('--pdt',
        help="the .pdt file used to define application sources and imported packages",
        metavar="FILE",
        required=True)      
parser.add_argument('--jobs',
        help="the number of make jobs to be run in parallel on Linux and "
                "macOS [default: 1]",
        metavar="NUMBER", type=int, default=1)
parser.add_argument('--qmake',
        help="the qmake executable when using an existing Qt installation",
        metavar="FILE")
parser.add_argument('--target', help="the target architecture", default='')
parser.add_argument('--reload-sysroot',
        help="Delete existing sysroot build folder and load target sysroot file",
        action='store_true')
parser.add_argument('--quiet', help="disable progress messages",
        action='store_true')
parser.add_argument('--verbose', help="enable verbose progress messages",
        action='store_true')
cmd_line_args = parser.parse_args()
pdt = os.path.abspath(cmd_line_args.pdt) if cmd_line_args.pdt else None
if not os.path.exists(pdt):
    print(f"[ERROR] Path to .pdt file {pdt} does not exist.", file=sys.stderr)
    print("Please specify a .pdt file that exists.")
    sys.exit(2)
jobs = cmd_line_args.jobs
qmake = os.path.abspath(cmd_line_args.qmake) if cmd_line_args.qmake else None
target = cmd_line_args.target
reload_sysroot = cmd_line_args.reload_sysroot
quiet = cmd_line_args.quiet
verbose = cmd_line_args.verbose

# State script args for debugging
print("\n----- REVIEWING COMMAND-LINE ARGS -----\n")
print(f"[INFO] The .pdt path received is: {pdt}")
print(f"[INFO] The number of jobs received is: {jobs}")
print(f"[INFO] The qmake path received is: {qmake}")
print(f"[INFO] The request to reload the sysroot is: {reload_sysroot}")
print(f"[INFO] The request to disable progress messages is: {quiet}")
print(f"[INFO] The request to enable verbose progress messages is: {verbose}")

print("\n----- INITIALISING AND COLLECTING VARIABLES -----\n")

# Initialise handy variables and tools
## Define pdt location as reference (for practicality)
pdt_dir = os.path.dirname(os.path.abspath(pdt))
print(f"[INFO] Pdt directory location is: {pdt_dir}. This is the reference directory.")
## Define default variable values
app_name_default = "MyCrossPlatformApp"
## Instantiate pdt_parser object
pdt_path = pdt
pdt_parser = pdtp.PdtParser(pdt_path)
## Get essential information from pdt file
sysroot_path = pdt_parser.get_sysroot_path()
print(f"[INFO] The sysroot path received is: {sysroot_path}")
app_name = pdt_parser.get_app_name()
if not app_name:
    print(f"[INFO] The application name has not been specified in the .pdt located at {pdt_path}")
    app_name = app_name_default
print(f"[INFO] Setting application name to: {app_name}")
app_entrypoint_name = pdt_parser.get_app_entry_point_script_name()
print(f"[INFO] The app entrypoint name received is: {app_entrypoint_name}")
app_package_dir = pdt_parser.get_app_package_path()
print(f"[INFO] The app package path received is: {app_package_dir}")
## Generate practical release directory structure
## By creating directories with date timestamp to store the app releases
current_datetime = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
app_release_dir = os.path.join(app_package_dir, os.path.pardir, 'releases', str(current_datetime)) 
print(f"[INFO] The app release dir is set to: {app_release_dir}")
os.makedirs(app_release_dir, exist_ok=True) 

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
os.chdir(pdt_dir)

print("\n----- BUILDING TARGET SYSROOT -----\n")

# Build the sysroot.
# This won't do anything if it is already built.
# Unless the reload_sysroot flag is set to True.

if reload_sysroot:
    shutil.rmtree('sysroot-' + target)
    shutil.rmtree('build-' + target)

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

args.append(sysroot_path)

run(args)

print("\n----- BUILDING THE PYQTDEPLOY PROJECT -----\n")

# Build the pyqtdeploy project
build_dir = 'build-' + target

args = ['pyqtdeploy-build', '--target', target, '--build-dir', build_dir]

if qmake:
    args.append('--qmake')
    args.append(qmake)

if quiet:
    args.append('--quiet')

if verbose:
    args.append('--verbose')

args.append(pdt_path)

run(args)

print("\n----- RUNNING QMAKE -----\n")

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
        if os.path.isfile('android-' + app_name + '-deployment-settings.json'):
            # Qt v5.14 or later.
            run([make, 'apk'])
            apk = app_name + '.apk'
            apk_dir = os.path.join(pdt_dir, build_dir, 'android-build')
        else:
            # Qt v5.13 or earlier.
            run([make, 'INSTALL_ROOT=' + app_entrypoint_name, 'install'])
            run([os.path.join(os.path.dirname(qmake_path), 'androiddeployqt'),
                    '--gradle', '--input',
                    'android-lib' + app_name + '.so-deployment-settings.json',
                    '--output', app_entrypoint_name])
            apk = app_entrypoint_name + '-debug.apk'
            apk_dir = os.path.join(pdt_dir, build_dir, app_entrypoint_name, 'build', 'outputs',
                    'apk', 'debug')

print("\n----- HANDLING APP OUTPUT -----\n")

# Re-centre folders around this current script
os.chdir(pdt_dir)

# Tell the user where the output app is.
if target.startswith('android'):
    # Copy the output app to the specified release directory
    shutil.copy(os.path.join(apk_dir, apk), app_release_dir)
    print(f"The released app {apk} can be found in {os.path.abspath(app_release_dir)}\n")
    print(f"""Debug tip: the {apk} file can also be found in the '{apk_dir}' directory. 
Run adb to install it to a simulator.""")

elif target.startswith('ios'):
    xcodeproj_app = app_entrypoint_name + '.xcodeproj'
    # Copy the output built app to the specified release directory
    shutil.copy(os.path.join(pdt_dir, build_dir, xcodeproj_app), app_release_dir)
    print(f"The released app {xcodeproj_app} can be found in {os.path.abspath(app_release_dir)}\n")
    print(f"""Debug tip: the {xcodeproj_app} file can be found in the '{build_dir}' directory.
Run Xcode to build the app and run it in the simulator or deploy it to a device.""")

elif target.startswith('win') or sys.platform == 'win32':
    # Copy the output built app to the specified release directory
    shutil.copy(os.path.join(pdt_dir, build_dir, app_entrypoint_name), app_release_dir)
    print(f"The released app {app_entrypoint_name} can be found in {os.path.abspath(app_release_dir)}\n")
    print(f"The {app_entrypoint_name} executable can be found in the '{os.path.join(build_dir, 'release')}' directory.")

else:
    # Copy the output built app to the specified release directory
    shutil.copy(os.path.join(pdt_dir, build_dir, app_entrypoint_name), app_release_dir)
    print(f"The released app {app_entrypoint_name} can be found in {os.path.abspath(app_release_dir)}\n")
    print(f"Debug tip: the {app_entrypoint_name} executable can be found in the '{build_dir}' directory.")
