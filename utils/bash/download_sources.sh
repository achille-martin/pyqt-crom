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

############################################
# PURPOSE
# -------
# Download external sources 
# required by the repo and its dependencies
############################################

# Create folder to hold the downloaded external sources
sources_folder_path="$PYQT_CROM_DIR/utils/resources"
mkdir -p $sources_folder_path

# Download the sources into the created folder
# if they have not been downloaded yet
cd $sources_folder_path
## Python
python_xz_file="Python-3.10.12.tar.xz"
if [[ -e $python_xz_file ]]; then
    printf "$python_xz_file is already downloaded into $sources_folder_path\n"
else
    wget https://www.python.org/ftp/python/3.10.12/$python_xz_file
    printf "Downloaded $python_xz_file into $sources_folder_path\n"
fi
## Qt
qt_xz_file="qt-everywhere-src-5.15.2.tar.xz"
if [[ -e $qt_xz_file ]]; then
    printf "$qt_xz_file is already downloaded into $sources_folder_path\n"
else
    wget https://download.qt.io/archive/qt/5.15/5.15.2/single/$qt_xz_file
    printf "Downloaded $qt_xz_file into $sources_folder_path\n"
fi
