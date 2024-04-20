#!/usr/bin/env bash

# MIT License

# Copyright (c) 2024 Achille MARTIN

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

##########################################
# Purpose
# -------
#
# Identify wheels 
# for desired non-standard python package
# with specific package version
# for the current OS specifications
##########################################

# Define a custom error handler function
handle_error() {
    echo "An error occurred: $1"
    exit 1
}

# Set the error handler to be called when an error occurs
trap 'handle_error "please review the input arguments"' ERR

# Ensure that package name is supplied
if [ "$#" -ne 2 ]
then
  echo "Usage: get_wheel_for_python_package.sh <python_package_name> <python_package_version>"
  exit 1
fi

python_package_name=$1
python_package_version=$2
echo "Python package deisred: $python_package_name"
echo "Python package version desired: $python_package_version"
echo "------"

# Create a temporary folder to download the wheels
temp_wheels_folder_path="$HOME/Downloads/temp_wheels"
mkdir -p $temp_wheels_folder_path

# Download the wheels for the current OS specifications
pip download --only-binary :all: --dest . --no-cache -d $temp_wheels_folder_path $python_package_name==$python_package_version

# Get the name of the wheels from the downloaded material
wheel_name=$(ls $temp_wheels_folder_path -tp | grep -v /$ | head -1)

# Possibility to remove the temporary wheel folder,
# but might look risky from a user perspective.
# User can manually delete the temporary folder if needed.

# Print out the name of the wheels
echo "------"
echo "Wheel name for Python package $python_package_name (version $python_package_version) and for current OS specifications is:"
echo "$wheel_name"
