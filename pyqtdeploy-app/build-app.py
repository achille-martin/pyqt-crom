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


def run(args):
    """ Run a command and terminate if it fails. """

    try:
        ec = subprocess.call(' '.join(args), shell=True)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
        ec = 1

    if ec:
        sys.exit(ec)

# Initialise handy variables
input_app_path_is_file = False
input_app_path_is_dir = False
build_app_name = 'example-pyqt5-app'

# Parse the command line.
parser = argparse.ArgumentParser()
parser.add_argument('--input-app-path', 
        help="the path to the app you want to build. \
                Make sure that the app path is the same as \
                the one entered in the `config-app.pdy` file.",
        default='')
parser.add_argument('--output-app-name',
        help="the desired name for your app. \
                It must be lowercase and dash-separated. \
                Make sure that you do not specify an app name \
                in the `config-app.pdy` file \
                and that you edit the `.py.dat` name.",
        default='')
parser.add_argument('--output-app-dir',
        help="the path to the desired directory \
                in which your built app will be saved",
        default='')
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
input_app_path = cmd_line_args.input_app_path
output_app_name = cmd_line_args.output_app_name
output_app_dir = cmd_line_args.output_app_dir
build_sysroot = not cmd_line_args.no_sysroot
installed_qt_dir = cmd_line_args.installed_qt_dir
source_dirs = cmd_line_args.source_dirs
target = cmd_line_args.target
quiet = cmd_line_args.quiet
verbose = cmd_line_args.verbose

# Request input and output app characteristics
# Request path for input app to build
if not input_app_path:
    print("Cannot find the desired path to an app to build. \
            Use --input-app-path if you want to specify one. \
            Otherwise, the default \
            `$SIMPLE_PYQT5_ANDROID_APP_DIR/example-pyqt5-app.py` \
            will be used.")
    # Ensure that the default input app path exists
    env_var_repo = os.environ.get('SIMPLE_PYQT5_ANDROID_APP_DIR') 
    if not env_var_repo:
        print("Cannot find the required environment variables. \
                Your environment has not been setup correctly, \
                please refer to the README.",
                file=sys.stderr)
        sys.exit(2)
    else:
        if not os.path.isfile(os.path.join(env_var_repo, 'example-pyqt5-app.py')):
            print("Cannot find a default app to build. \
                    Your environment has not been setup correctly, \
                    please refer to the README.",
                    file=sys.stderr)
            sys.exit(2)
        else:
            input_app_path = os.path.join(env_var_repo, 'example-pyqt5-app.py')
            input_app_path_is_file = True
else:
    # Ensure that the input app path exists
    if os.path.isfile(input_app_path):
        input_app_path_is_file = True
    elif os.path.isdir(input_app_path):
        input_app_path_is_dir = True
        print("Cannot handle input app path as directory yet.",
                file=sys.stderr)
        sys.exit(2)
    else:
        print("Cannot find the specified path to the app to build. \
                Please review the --input-app-path argument.",
                file=sys.stderr)
        sys.exit(2)
# Request name for output built app
if not output_app_name:
    print("Cannot find a desired name for the built app. \
            Use --output-app-name if you want to specify one. \
            Otherwise, the default name `built-app` will be used")
    output_app_name="ExamplePyQt5AndroidApp"
# Request path to directory to save output built app
if not output_app_dir:
    print("Cannot find a path to the desired directory \
            in which the built app will be saved. \
            Use --output-app-dir if you want to specify one. \
            Otherwise, the same directory as the app to build will be used.")
    # Extract directory path from input app path
    if input_app_path_is_file:
        output_app_dir = os.path.split(input_app_path)[0]
    elif input_app_path_is_dir:
        output_app_dir = input_app_path
    else:
        pass
else:
    # Ensure output dir path exists
    if not os.path.isdir(output_app_dir):
        print("Cannot find the path to the output app directory. \
                Please review the argument --output-app-dir.")

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
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
shutil.copy(input_app_path, os.path.join('data', build_app_name + '.py.dat'))

run(['pyqtdeploy-build', '--target', target, '--sysroot', sysroot_dir,
            '--build-dir', build_dir, 'config-app.pdy'])

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
        run([make, 'INSTALL_ROOT=' + build_app_name, 'install'])
        run([os.path.join(host_bin_dir, 'androiddeployqt'), '--gradle',
                '--input', 'android-lib' + output_app_name + '.so-deployment-settings.json',
                '--output', build_app_name])

# Tell the user where the output built app is.
if target.startswith('android'):
    apk_dir = os.path.join(env_var_repo, 'pyqtdeploy-app', build_dir, build_app_name, 'build', 'outputs', 'apk',
            'debug')
    output_app_full_name = build_app_name + '-debug.apk'
    print("""The '{0}' file can be found in the '{1}'
directory.  Run adb to install it to a simulator.""".format(output_app_full_name, apk_dir))
    # Copy the output built app to the specified or default path
    shutil.copy(os.path.join(apk_dir, output_app_full_name), output_app_dir)
    os.rename(os.path.join(output_app_dir, output_app_full_name), os.path.join(output_app_dir, output_app_name + '.apk'))

elif target.startswith('ios'):
    output_app_full_name = build_app_name + '.xcodeproj'
    print("""The '{0}' file can be found in the '{1}' directory.
Run Xcode to build the app and run it in the simulator or deploy it to a
device.""".format(output_app_full_name, build_dir))
    # Copy the output built app to the specified or default path
    shutil.copy(os.path.join(build_dir, output_app_full_name), output_app_dir)

elif target.startswith('win') or sys.platform == 'win32':
    output_app_full_name = build_app_name
    output_dir_default = os.path.join(build_dir, 'release')
    print("The '{0}' executable can be found in the '{1}' directory.".format(output_app_full_name, output_dir_default))
    # Copy the output built app to the specified or default path
    shutil.copy(os.path.join(output_dir_default, output_app_full_name), output_app_dir)

else:
    output_app_full_name = build_app_name
    print("The '{0}' executable can be found in the '{1}' directory.".format(output_app_full_name, build_dir))
    # Copy the output built app to the specified or default path
    shutil.copy(os.path.join(build_dir, output_app_full_name), output_app_dir)

