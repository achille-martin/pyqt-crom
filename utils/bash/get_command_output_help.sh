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

#########################################################
# PURPOSE
# -------
# Collect information about a command
# for help and debugging purposes
#
# INPUTS
# ------
# * Command to collect help and debug information about
# * Additional relevant files to boost help
#
# OUTPUTS
# -------
# * Markdown file containing:
#   * Information about source OS
#   * Information about python
#   * Information about repo
#   * Information about dependencies
#       * Get venv/ file architecture for instance
#       * Get resources/ content for instance
#   * Information about command input
#########################################################

# Define print usage function
print_usage() {
    printf "Usage: get_command_output_help.sh \"<command_to_run>\" -f \"<file_to_include_1> ... <file_to_include_n>\"\n"
}

# Ensure correct number of required arguments is supplied
if [[ "$#" -lt 1 ]]; then
    print_usage
    exit 1
fi

# Get optional arguments
flags="f:"
OPTIND=2
file_input=()
while getopts $flags flag; do
    case "${flag}" in
        f) file_input+=( "${OPTARG}" ) ;;
        *) print_usage; exit 1 ;;
    esac
done

# Ensure that the required arguments are correctly supplied
if [[ "$1" == "-f"  ]]; then
    printf "First required argument is not valid: $1\n"
    print_usage
    exit 1
fi

# Define handy variables
code_snippet_start="\n \`\`\` \n"
code_snippet_end=$code_snippet_start

# Create log folder if not already created
log_folder="$PYQT_CROM_DIR/log"
mkdir -p $log_folder

# Change directory to log folder for practicality
cd $log_folder

# Create file to hold information
current_date_time=$(date +"%Y_%m_%d-%H_%M_%S")
log_file="command_output_help_$current_date_time.md"

printf "[INFO] Creating file $log_file in $log_folder to hold information...\n"

touch $log_file

printf "[INFO] ...Done.\n"

# Pre-populate the log file with relevant information about the request
printf "[INFO] Populating file with relevant information about the request...\n"

printf "# Command output help\n" >> $log_file 2>&1
printf "\n## Request information\n\n" >> $log_file 2>&1
printf "* Command requested: $code_snippet_start XXX $code_snippet_end" >> $log_file 2>&1
printf "* Date and time requested at: $code_snippet_start $current_date_time $code_snippet_end\n"  >> $log_file 2>&1
printf "* User emitting request: $code_snippet_start $USER $code_snippet_end\n" >> $log_file 2>&1

printf "[INFO] ...Done.\n"

# Get context information to understand the command output

## Get information about source OS
printf "[INFO] Populating file with information about source OS...\n"

printf "\n## Source OS information\n" >> $log_file 2>&1
os_pretty_name=$(cat "/etc/os-release" | grep "PRETTY_NAME")
printf "* Source OS pretty name: $code_snippet_start $os_pretty_name $code_snippet_end\n" >> $log_file 2>&1

printf "[INFO] ...Done.\n"

## Get information about python in virtual environment
printf "[INFO] Populating file with information about python...\n"

source $PYQT_CROM_DIR/venv/pyqt-crom-venv/bin/activate
python_version=$(python --version)
pip_version=$(pip --version)
pip_packages_installed=$(pip list --local)
pip_dependency_tree=$(pipdeptree --local)

printf "\n## Python information\n" >> $log_file 2>&1
printf "* Python version: $code_snippet_start $python_version $code_snippet_end\n" >> $log_file 2>&1
printf "* Pip version: $code_snippet_start $pip_version $code_snippet_end\n" >> $log_file 2>&1
printf "* Pip packages installed: $code_snippet_start $pip_packages_installed $code_snippet_end\n" >> $log_file 2>&1
printf "* Pip dependency tree: $code_snippet_start $pip_dependency_tree $code_snippet_end\n" >> $log_file 2>&1

printf "[INFO] ...Done.\n"

## Get information about the general repo
printf "[INFO] Populating file with information about repo...\n"

printf "[INFO] ...Done.\n"

## Get information about repo dependencies
printf "[INFO] Populating file with information about repo dependencies...\n"

printf "[INFO] ...Done.\n"

# Get information about the command input
printf "[INFO] Populating file with information about command input...\n"

printf "[INFO] ...Done.\n"

# Append extra file content
printf "[INFO] Populating file with extra input file content...\n"

printf "[INFO] ...Done.\n"

