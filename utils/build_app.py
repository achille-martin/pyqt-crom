# Copyright (c) 2019, Riverbank Computing Limited
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
import utils.pdy_parser as pdyp
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

# Initialise handy variables and tools
## Define current script location as reference
script_dir = os.path.dirname(os.path.realpath(__file__))
## Define default variable values
app_name_default = "MyApp"
app_release_dir_default = script_dir
## Instantiate pdy_parser object
pdy_path = os.path.join(script_dir, 'config_app.pdy')
if not os.path.exists(pdy_path):
    print("[ERROR] Cannot find .pdy at location: " + str(pdy_path), file=sys.stderr)
    sys.exit(2)
pdy_parser = pdyp.PdyParser(pdy_path)
## Get essential information from pdy file
app_name = pdy_parser.get_app_name()
if not app_name:
    print("[INFO] The application name has not been specified in the .pdy located at " + str(pdy_path))
    app_name = app_name_default
    print("[INFO] Setting the application name to `" + str(app_name) + "`")
app_entrypoint_name = pdy_parser.get_app_entrypoint_script_name()
if not app_entrypoint_name:
    print("[ERROR] The entrypoint has not been specified in the .pdy", file=sys.stderr)
    print("Please add an entrypoint to the .pdy located at: " + str(pdy_path))
    sys.exit(2)
app_package_dir = pdy_parser.get_app_package_path()
if not app_package_dir:
    print("[ERROR] The package directory has not been specified in the .pdy", file=sys.stderr)
    print("Please select your package in the .pdy located at: " + str(pdy_path))
    sys.exit(2)
## Generate practical directory structure
## Create directories with date timestamp to store the app releases
current_datetime = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
app_release_dir = os.path.join(app_package_dir, 'releases', str(current_datetime)) 
os.makedirs(app_release_dir, exist_ok=True) 

# Parse the command line.
parser = argparse.ArgumentParser()
parser.add_argument('--installed-qt-dir',
        help="the name of a directory containing pre-built Qt installations",
        metavar="DIR")
parser.add_argument('--no-sysroot', help="do not build the sysroot",
        action='store_true')
parser.add_argument('--source-dir',
        help="a directory containing the source packages", metavar="DIR",
        dest='source_dirs', action='append')
parser.add_argument('--target', help="the target platform", default='')
parser.add_argument('--quiet', help="disable progress messages",
        action='store_true')
parser.add_argument('--verbose', help="enable verbose progress messages",
        action='store_true')
cmd_line_args = parser.parse_args()
build_sysroot = not cmd_line_args.no_sysroot
installed_qt_dir = cmd_line_args.installed_qt_dir
source_dirs = cmd_line_args.source_dirs
target = cmd_line_args.target
quiet = cmd_line_args.quiet
verbose = cmd_line_args.verbose

# Pick a default target if none is specified.
if not target:
    if sys.platform == 'win32':
        # MSVC2015 is v14, MSVC2017 is v15.
        vs_major = os.environ.get('VisualStudioVersion', '0.0').split('.')[0]

        if vs_major == '15':
            is_32 = (os.environ.get('VSCMD_ARG_TGT_ARCH') != 'x64')
        elif vs_major == '14':
            is_32 = (os.environ.get('Platform') != 'X64')
        else:
            # Default to 64 bits.
            is_32 = False

        target = 'win-' + ('32' if is_32 else '64')
    elif sys.platform == 'darwin':
        target = 'macos-64'
    elif sys.platform.startswith('linux'):
        import struct

        target = 'linux-{0}'.format(8 * struct.calcsize('P'))
    else:
        print("Unsupported platform:", sys.platform, file=sys.stderr)
        sys.exit(2)

# Make sure the Qt directory was specified if it is needed.
if target in ('android-32', 'android-64', 'ios-64') and not installed_qt_dir:
    print("--installed-qt-dir must be specified for", target, file=sys.stderr)
    sys.exit(2)

# Create the list of directories to search for source packages and Qt.
if not source_dirs:
    source_dirs = ['.']

if installed_qt_dir:
    source_dirs.insert(0, installed_qt_dir)

source_dirs = [os.path.abspath(s) for s in source_dirs]

# Anchor everything from the directory containing this script.
current_script_location = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_script_location)

sysroot_dir = 'sysroot-' + target
build_dir = 'build-' + target
host_bin_dir = os.path.abspath(os.path.join(sysroot_dir, 'host', 'bin'))

# Build sysroot.
if build_sysroot:
    args = ['pyqtdeploy-sysroot', '--target', target, '--sysroot', sysroot_dir]

    for s in source_dirs:
        args.append('--source-dir')
        args.append(s)

    if quiet:
        args.append('--quiet')

    if verbose:
        args.append('--verbose')

    args.append('sysroot.json')

    run(args)

# Build the demo.
run(['pyqtdeploy-build', '--target', target, '--sysroot', sysroot_dir,
            '--build-dir', build_dir, str(pdy_path)])

# Run qmake.  Use the qmake left by pyqtdeploy-sysroot.
os.chdir(build_dir)
run([os.path.join(host_bin_dir, 'qmake')])

# Run make. (When targeting iOS we leave it to Xcode.)
if target.startswith('ios'):
    pass
else:
    # We only support MSVC on Windows.
    make = 'nmake' if sys.platform == 'win32' else 'make'

    run([make])
    
    if target.startswith('android'):
        qt_old_version_flag = 1
        if os.path.isfile('android-' + app_name + '-deployment-settings.json'):
            # Qt v5.14 or later
            print("Qt v5.14 or later DETECTED")
            run([make, 'apk', '--debug'])
            qt_old_version_flag = 0
        else:
            # Qt v5.13 or earlier
            print("Qt v5.13 or earlier DETECTED")
            run([make, 'INSTALL_ROOT=' + app_entrypoint_name, 'install'])
            run([os.path.join(host_bin_dir, 'androiddeployqt'), '--gradle', '--verbose',
                    '--input', 'android-lib' + app_name + '.so-deployment-settings.json',
                    '--output', app_entrypoint_name])
            qt_old_version_flag = 1

# Re-centre folders around this script in case current directory has been modified
os.chdir(current_script_location)

# Tell the user where the output built app is.
if target.startswith('android'):
    if qt_old_version_flag:
        output_app_name = app_entrypoint_name + '-debug.apk'
        output_app_dir = os.path.join(script_dir, build_dir, app_entrypoint_name, 'build', 'outputs', 'apk',
                'debug')
        print("""The '{0}' file can be found in the '{1}'
    directory.  Run adb to install it to a simulator.""".format(output_app_name, output_app_dir))
        # Copy the output app to the specified release directory
        shutil.copy(os.path.join(output_app_dir, output_app_name), app_release_dir)
        os.rename(os.path.join(app_release_dir, output_app_name), os.path.join(app_release_dir, app_name + '.apk'))
        print("\nThe released app " + app_name + ".apk" + " can be found in " + app_release_dir)
    else:
        output_app_name = app_name + '.apk'
        output_app_dir = os.path.join(build_dir, 'android-build')
        print("""The '{0}' file can be found in the '{1}'
    directory.  Run adb to install it to a simulator.""".format(output_app_name, output_app_dir))
        # Copy the output app to the specified release directory
        shutil.copy(os.path.join(output_app_dir, output_app_name), app_release_dir)
        print("\nThe released app " + output_app_name + " can be found in " + app_release_dir)


elif target.startswith('ios'):
    output_app_name = app_entrypoint_name + '.xcodeproj'
    print("""The '{0}' file can be found in the '{1}' directory.
Run Xcode to build the app and run it in the simulator or deploy it to a
device.""".format(output_app_name, build_dir))
    # Copy the output built app to the specified release directory
    shutil.copy(os.path.join(build_dir, output_app_name), app_release_dir)

elif target.startswith('win') or sys.platform == 'win32':
    output_app_name = app_entrypoint_name
    output_app_dir = os.path.join(build_dir, 'release')
    print("The '{0}' executable can be found in the '{1}' directory.".format(output_app_name, output_app_dir))
    # Copy the output built app to the specified release directory
    shutil.copy(os.path.join(output_app_dir, output_app_name), app_release_dir)

else:
    output_app_name = app_entrypoint_name
    print("The '{0}' executable can be found in the '{1}' directory.".format(output_app_name, build_dir))
    # Copy the output built app to the specified release directory
    shutil.copy(os.path.join(build_dir, output_app_name), app_release_dir)

