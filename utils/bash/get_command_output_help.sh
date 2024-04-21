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

# Ensure that the required arguments are correctly supplied
command_to_run="$1"
if [[ "$command_to_run" == "-f"*  ]]; then
    printf "First required argument is not valid: $1\n"
    print_usage
    exit 1
fi

# Get optional arguments
flags="f:"  # Expected arguments for `f` flag
OPTIND=2  # Ignore the first required argument
file_input_list=()
while getopts $flags flag; do
    case "${flag}" in
        f) file_input_list+=( "${OPTARG}" ) ;;
        *) print_usage ; exit 1 ;;
    esac
done

# Define handy variables
code_snippet_start="\n \`\`\` \n"
code_snippet_end=$code_snippet_start
text_to_add=""

# Create log folder if not already created
log_folder="$PYQT_CROM_DIR/log"
mkdir -p $log_folder

# Create file to hold information
current_date_time=$(date +"%Y_%m_%d-%H_%M_%S" |& tee '/dev/null')
log_file_name="command_output_help_$current_date_time.md"
log_file_path="$log_folder/$log_file_name"

printf "[INFO] Creating file $log_file_path to hold information...\n"

touch $log_file_path

printf "[INFO] ...Done.\n"

# Pre-populate the log file with relevant information about the request
printf "[INFO] Populating file with relevant information about the request...\n"

current_working_directory=$(pwd |& tee '/dev/null')
text_to_add="# Command output help

## Request information
* Command requested: $code_snippet_start $command_to_run $code_snippet_end
* Current working directory: $code_snippet_start $current_working_directory $code_snippet_end
* Date and time requested at: $code_snippet_start $current_date_time $code_snippet_end
* User emitting request: $code_snippet_start $USER $code_snippet_end
"
printf "$text_to_add" >> $log_file_path 2>&1

printf "[INFO] ...Done.\n"

# Get context information to understand the command output

## Get information about source OS
printf "[INFO] Populating file with information about source OS...\n"

os_pretty_name=$(cat "/etc/os-release" | grep "PRETTY_NAME" |& tee '/dev/null')
text_to_add="## Source OS information
* Source OS pretty name: $code_snippet_start $os_pretty_name $code_snippet_end
"
printf "$text_to_add" >> $log_file_path 2>&1

printf "[INFO] ...Done.\n"

## Get information about python in virtual environment
printf "[INFO] Populating file with information about python...\n"

source $PYQT_CROM_DIR/venv/pyqt-crom-venv/bin/activate
python_version=$(python --version |& tee '/dev/null')
pip_version=$(pip --version |& tee '/dev/null')
pip_packages_installed=$(pip list --local |& tee '/dev/null')
pip_dependency_tree=$(pipdeptree --local |& tee '/dev/null')

text_to_add="## Python information
* Python version: $code_snippet_start $python_version $code_snippet_end
* Pip version: $code_snippet_start $pip_version $code_snippet_end
* Pip packages installed: $code_snippet_start $pip_packages_installed $code_snippet_end
* Pip dependency tree: $code_snippet_start $pip_dependency_tree $code_snippet_end
"
printf "$text_to_add" >> $log_file_path 2>&1

printf "[INFO] ...Done.\n"

## Get information about the general repo
printf "[INFO] Populating file with information about repo...\n"

git_branch_current=$(git branch --show-current |& tee '/dev/null')
latest_commit_date=$(git log -1 --format=%cd |& tee '/dev/null')
environment_variables=$(cat $PYQT_CROM_DIR/utils/bash/setup_path.sh |& tee '/dev/null')

text_to_add="## General repo information
* Git branch: $code_snippet_start $git_branch_current $code_snippet_end
* Latest git commit date: $code_snippet_start $latest_commit_date $code_snippet_end
* Environment variables: $code_snippet_start $environment_variables $code_snippet_end
"
printf "$text_to_add" >> $log_file_path 2>&1

printf "[INFO] ...Done.\n"

## Get information about repo dependencies
printf "[INFO] Populating file with information about repo dependencies...\n"

external_sources_list=$(ls -l $PYQT_CROM_DIR/utils/resources |& tee '/dev/null')

text_to_add="## Repo dependency information
* External sources: $code_snippet_start $external_sources_list $code_snippet_end
"
printf "$text_to_add" >> $log_file_path 2>&1

printf "[INFO] ...Done.\n"

# Get information about the command input
printf "[INFO] Populating file with information about command input...\n"

text_to_add="## Command input information
* Command run: $code_snippet_start $(eval $command_to_run |& tee '/dev/null') $code_snippet_end
"
printf "$text_to_add" >> $log_file_path 2>&1

printf "[INFO] ...Done.\n"

# Append extra file content
printf "[INFO] Populating file with extra input file content...\n"

text_to_add="## Extra file content information
"
printf "$text_to_add" >> $log_file_path 2>&1
for file_path in $file_input_list; do
    file_content=$(cat $file_path |& tee '/dev/null')
    printf "* File \`$file_path\`: $code_snippet_start $file_content $code_snippet_end\n" >> $log_file_path 2>&1
done

printf "[INFO] ...Done.\n"

