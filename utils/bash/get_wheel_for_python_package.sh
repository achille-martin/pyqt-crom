#!/usr/bin/env bash

# Purpose:
# Identify wheels for desired non-standard python package
# for the current OS specifications

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

# Create a temporary folder to download the wheels
mkdir -p $HOME/Downloads/temp_wheels

# Download the wheels for the current OS specifications
pip download --only-binary :all: --dest . --no-cache -d $HOME/Downloads/temp_wheels $python_package_name==$python_package_version

# Get the name of the wheels from the downloaded material
wheel_name=$(ls $HOME/Downloads/temp_wheels -tp | grep -v /$ | head -1)

# Possibility to remove the temporary wheel folder,
# but might look risky from a user perspective.
# User can manually deleted if needed.

# Print out the name of the wheels
echo "------"
echo "Wheel name for Python package $python_package_name (version $python_package_version) and for current OS specifications is:"
echo "$wheel_name"
