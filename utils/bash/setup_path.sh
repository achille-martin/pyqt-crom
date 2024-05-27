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
# PURPOSE
# -------
# Setup handy path variables
# for the repo and its dependencies
##########################################

export PYQT_CROM_DIR=$HOME/Documents/pyqt-crom
export RESOURCES_DIR=$PYQT_CROM_DIR/utils/resources
export QT_DIR=$HOME/Qt5.15.2/5.15.2
export ANDROID_SDK_ROOT=$HOME/Android/Sdk
export ANDROID_NDK_ROOT=$ANDROID_SDK_ROOT/ndk/21.4.7075529
export ANDROID_NDK_PLATFORM=android-28
# export ANDROID_NDK_HOST=linux-x86_64
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export JAVA_JRE=/usr/lib/jvm/java-11-openjdk-amd64/jre
export PATH=$PATH:$JAVA_HOME/bin
