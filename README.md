# Simple PyQt5 Android App

<a id="purpose"></a>
## Purpose 

:dart: The aim of this repo is to create an android app (.apk) from a (simple) PyQt5 app.

<a id="toc"></a>
## Table of Contents

1. [Purpose](#purpose)
1. [Example App Demo](#example-demo-app)
    1. [Review the pre-requisites](#pre-requisites)
    1. [Setup the path to the app folder](#path-setup)
    1. [Download the github repo](#github-repo-download)
    1. [Setup the virtual environment for your app](#virtual-environment-setup)
    1. [Install the external dependencies](#external-dependency-installation)
    1. [Setup the environment variables](#environment-variable-setup)
    1. [Build the .apk with pyqtdeploy](#apk-build)
    1. [Test the .apk](#apk-test)
    1. [Customise the app for Android (OPTIONAL)](#app-customisation)
    1. [PyQt5 modules and features (OPTIONAL)](#pyqt5-modules-and-features)
1. [Detailed build from a complex pyqt-demo app](#detailed-complex-build))

<a id="example-demo-app"></a>
## Example Demo App 

:mag: _This section explains the process to generate an .apk for a simple pyqt5 demo app._

<a id="pre-requisites"></a>
### Review the pre-requisites 

Specs of Linux machine used:
* Ubuntu 18.04
* Python 3.6.9

:bulb: _Refer to [Virtualbox Setup](#virtualbox-setup) if you don't have a Linux OS available._

Specs of target machine desired:
* Android 9.0 (at least)

[:arrow_heading_up: Back to TOP](#toc) 

<a id="path-setup"></a>
### Setup the path to the app folder

:warning: _We will use `$SIMPLE_PYQT5_ANDROID_APP_DIR` as the variable containing the path to the app folder._

Add the variable to your `.bashrc` with:

```
printf "%s\n" \
"" \
"# Environment variable for Simple PyQt5 Android App path" \
"export SIMPLE_PYQT5_ANDROID_APP_DIR=$HOME/Documents/simple-pyqt5-android-app" \
"" \
>> $HOME/.bashrc
source $HOME/.bashrc
```

[:arrow_heading_up: Back to TOP](#toc) 

<a id="github-repo-download"></a>
### Download the github repo 

```
cd $HOME/Documents
git clone git@github.com:achille-martin/simple-pyqt5-android-app.git
```

[:arrow_heading_up: Back to TOP](#toc) 

<a id="virtual-environment-setup"></a>
### Setup the virtual environment for your app 

1) Create a virtual environment with your python3 installed on your computer

```
sudo apt-get update
sudo apt-get install python3-pip
pip3 install virtualenv
cd $SIMPLE_PYQT5_ANDROID_APP_DIR
mkdir -p venv
cd venv
virtualenv simple-pyqt5-android-app-venv -p python3
```

2) Activate your virtual environment

```
source $SIMPLE_PYQT5_ANDROID_APP_DIR/venv/simple-pyqt5-android-app-venv/bin/activate
```

:bulb: _To exit the virtual environment, type in your terminal `deactivate`._

3) Install the necessary pip packages

```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR
pip3 cache purge
pip3 install -r requirements.txt
```

:bulb: _You can confirm your pip packages with `pip3 list --local`._

4) Test the PyQt5  app in your virtual environment

```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR
python3 example-pyqt5-app.py
```

The PyQt5 app will start and you can confirm that it is displayed properly on the machine used:
- Click the button
- An alert message is displayed stating that you have clicked the button

[:arrow_heading_up: Back to TOP](#toc) 

<a id="external-dependency-installation"></a>
### Install the external dependencies

1) Download a set of external dependencies

Download the sources with:

```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/resources
chmod +x download_sources.sh
./download_sources.sh
```

:point_up: _You can confirm that the list of packages required matches with the versions from `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/sysroot.json`._

2) Install Qt from the installer

Download the version which matches the one in `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/sysroot.json`:

```
sudo apt-get install wget
cd $HOME/Downloads
wget https://download.qt.io/archive/qt/5.12/5.12.2/qt-opensource-linux-x64-5.12.2.run
chmod +x qt*.run
./qt-opensource-linux-x64-5.12.2.run
```

A Qt window will appear on which you can sign up:
- Verify your email and register as an individual (no need for location)
- Restart the Qt installer with: `./qt-opensource-linux-x64-5.12.2.run`
- Log in, state that you are an individual and not a company
- Setup will start
- Select folder location `$HOME/Qt5.12.2`
- Installation will start

:memo: _If custom installation has to be selected, make sure you only setup `Qt5.12.2` and the default packages._

:hand: _Make sure that you can access `$HOME/Qt5.12.2/5.12.2` and that the folder `android_arm64_v8a` is located inside of it._

3) Install Android Studio

Download Android Studio (latest version) from either https://developer.android.com/studio, or get the version `2022.2.1.18` used for this repo (at the time of writing):

```
cd $HOME/Downloads
wget https://redirector.gvt1.com/edgedl/android/studio/ide-zips/2022.2.1.18/android-studio-2022.2.1.18-linux.tar.gz
```

Move the contents of the downloaded `tar.gz` to your `$HOME` directory using:

```
cd $HOME/Downloads
tar -xvf android-studio-2022.2.1.18-linux.tar.gz
mv android-studio $HOME
```

Start the installation with:

```
cd $HOME/android-studio/bin
./studio.sh
```

The Android Studio installer will start:
* Do not import settings
* Select custom installation if possible
* Deselect Virtual Device if you don't need it for testing
* Keep a note of the Sdk installation path, which should be `$HOME/Android/Sdk`
* Start the download (unless you want to install extra features)

:hand: _Make sure that the default SDK has been installed in `$HOME/Android/Sdk` and that `$HOME/Android/Sdk/platforms` contains `android-28` folder only.
If not, follow the instructions at the next step to set things up correctly._

4) Install correct Android SDK and Tools

* Restart Android Studio with `cd $HOME/android-studio/bin && ./studio.sh` (skip if no SDK found)
* On the menu screen, click on "more options" and then "SDK manager"
* At this point, it is recommended to use MAX Android v9.0 (Pie) = android-28 because it is the latest version of the working NDK (v19)

:thought_balloon: _It might be possible to install a later NDK and thus a later android version_

* Confirm that the right SDK has been installed and get the API level (in the example, 28)
    * Make sure that in the `SDK Platforms` tab, the following is installed: (Android 9.0) Android SDK Platform 28, (Android 9.0) Sources for Android 28.
    * Remove any additional unneeded package from the list.
    * Make sure that in the `SDK Tools` tab, the following is installed (you might need to untick Hide Obsolete Packages and tick Show Package Details): (Android SDK Build-Tools 34-rc3) 33.0.2, Android Emulator, Android SDK Platform-tools, Android SDK Tools (Obsolete)

* Close Android Studio

5) Install Android NDK matching with Qt version

Download NDK 19c using:

```
cd $HOME/Downloads
wget https://dl.google.com/android/repository/android-ndk-r19c-linux-x86_64.zip
```

:thought_balloon: _This NDK is known to be working with Qt5.12.2, but there might be others._

Extract the contents of the downloaded `.zip` into `$HOME/Android` using:

```
cd $HOME/Downloads
sudo apt-get install unzip
unzip android-ndk-r19c-linux-x86_64.zip
mv android-ndk-r19c/ $HOME/Android
```

:hand: _Make sure that `~/Android/android-ndk-r19c/platforms` contains the folder `android-28`._

6) Install Java for Android Studio

Install a stable java jdk available for your Ubuntu distribution and tested with Gradle:

```
sudo apt install openjdk-8-jdk openjdk-8-jre
```

:hand: *Confirm the version with `java -version` which should be `v1.8.0_362`.*

[:arrow_heading_up: Back to TOP](#toc) 

<a id="environment-variable-setup"></a>
### Setup the environment variables

Load the environment variables on terminal startup with:

```
printf "%s\n" \
"" \
"# Load extra environment variables for Simple PyQt5 Android App" \
"source $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/resources/path_setup.sh" \
"" \
>> $HOME/.bashrc
source $HOME/.bashrc
```

[:arrow_heading_up: Back to TOP](#toc) 

<a id="apk-build"></a>
### Build the .apk with pyqtdeploy

Start the building process of the .apk with:

```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app
python3 build-app.py --target android-64 --source-dir $RESOURCES_DIR --installed-qt-dir $QT_DIR --verbose
``` 
:hourglass_flowing_sand: _Let the app build (it may take a while)_

:tada: _The app is built when you see "BUILD SUCCESSFUL"_

[:arrow_heading_up: Back to TOP](#toc) 

<a id="apk-test"></a>
### Test the .apk 

The generated `example-pyqt5-app-debug.apk` can be found in `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/build-android-64/example-pyqt5-app/build/outputs/apk/debug`

You can then either:
* Copy, install and run the .apk onto your phone (>=Android v9.0)
* Install BlueStacks on Windows (https://www.bluestacks.com/download.html), enable hyper-V, open `my games` and install the .apk, run the app offline

[:arrow_heading_up: Back to TOP](#toc) 

<a id="app-customisation"></a>
### Customise the app for Android (OPTIONAL) 

Refer to "Adding Android specific things" in https://github.com/kviktor/pyqtdeploy-android-build.

[:arrow_heading_up: Back to TOP](#toc) 

<a id="pyqt5-modules-and-features"></a>
### PyQt5 modules and features (OPTIONAL) 

1) Add images

Use QPixmap and pyrcc to save images and render them.

2) Manage your python app in android

Review python modules to create a structured project folder with writable paths.

[:arrow_heading_up: Back to TOP](#toc) 

<a id="detailed-complex-build"></a>
## Detailed build from a complex pyqt-demo app

_This section explains how to create an .apk from the more complex pyqt-demo app._

<a id="pre-requisites-complex"></a>
### Review the pre-requisites

Get rid of `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app` folder:

```
sudo rm -r $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app
```

[:arrow_heading_up: Back to TOP](#toc) 

<a id="build-files-complex"></a>
### Get the build files for pyqtdeploy

1) Get the pyqt-demo folder

- Download the pyqt-demo folder from: https://pypi.org/project/pyqtdeploy/2.5.1/#files

_Note: make sure that you get the matching pyqtdeploy version you installed with pip_

_Note2: stick to v2.x as v3.x had some major changes which will generate loads of issues_

2) Extract the contents of the `.tar.gz`

- Copy the contents into `$SIMPLE_PYQT5_ANDROID_APP_DIR`

*Note: you should now have a folder called `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-2.5.1`*

[:arrow_heading_up: Back to TOP](#toc) 

<a id="folder-setup-complex"></a>
### Setup your app folder to build an apk with pyqtdeploy

1) Create new folder called `pyqtdeploy-app`

```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR
mkdir pyqtdeploy-app
```

- Copy the contents of `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-2.5.1/demo` into `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app`
- Delete `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/pyqt-demo.py`
- Rename `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/build-demo.py` into `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/build-app.py`
- Replace the line `shutil.copy('pyqt-demo.py', os.path.join('data', 'pyqt-demo.py.dat'))` in `build-app.py` with:
```
shutil.copy('../example-pyqt5-app.py', os.path.join('data', 'example-pyqt5-app.py.dat'))
```
- Rename all occurrences of `pyqt-demo` into `example-pyqt5-app` in `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/build-app.py`
- Rename `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/pyqt-demo.pdy` into `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy`
- Update the `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy` with the necessary packages:
```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app
pyqtdeploy example-pyqt5-app.pdy
```
- Update the location of the main script file in `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy`: use the file explorer to find `example-pyqt5-app.py`
- Rename `pyqt-demo.py.dat` inside of `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy` with vim into: `example-pyqt5-app.py.dat`
- Check your python version (in your virtual environment) and make the version in `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy` match: select the right one
- In the PyQt Modules tab of `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy`, select your relevant Qt modules. For instance: QtCore, QtWidgets.

_Note that the .pdy might force include some default Qt modules like: QtGui, sip_

- In the Standard Library tab of `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy`, remove all the extra modules and keep only the default ones. If needed for your app, add more.

- Update `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/sysroot.json` to reflect the packages selected in `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy` and the desired versions
- Remove the following packages (for the example) from `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/sysroot.json`: openssl, zlib, pyqt3d, pyqtchart, pyqtdatavisualization, pyqtpurchasing, qscintilla
- Keep the following packages (for the example) in `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/sysroot.json`: qt5 version 5.12.2, python update to version 3.6.9 (the version in your virtual environment), sip version 4.19.15, pyqt5 version 5.12.1 (even though v.5.15.6 installed in virtual environment)
- in pyqt5 section of `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/sysroot.json`, update the list of android modules to match `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy`:
```
        "android#modules":              [
                "QtCore", "QtGui", "QtWidgets"
        ],
```

[:arrow_heading_up: Back to TOP](#toc) 

<a id="setup-build-test-complex"></a>
### Setup, build and test the app

Please follow the steps in section "Example App Demo" to setup, build and test your own pyqt5 app.

[:arrow_heading_up: Back to TOP](#toc) 

<a id="virtualbox-setup"></a>
## Setup in VirtualBox

When setting the repo up in VirtualBox, you might come across the following issues:

1) Issue with `xcb`

The error message is likely to be:
```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
```

First, enable the Qt debug prints:
```
export QT_DEBUG_PLUGINS=1
```

Second, identify the issue.
If it is related to the package `libxcb-xinerama`, then:
```
sudo apt-get install libxcb-xinerama0
``` 

[:arrow_heading_up: Back to TOP](#toc) 

<a id="credits"></a>
## Credits

_This section details the main contributors and sources for the creation of the repo._

Repository created by Achille Martin.

Donations accepted as hard work has been put into this repository, and if you feel you can make progress with your projects by converting your pyqt5 apps into Android apps.

Inspiration from:
- https://github.com/kviktor/pyqtdeploy-android-build
- https://medium.com/@Lola_Dam/packaging-pyqt-application-using-pyqtdeploy-for-both-linux-and-android-32ac7824708b

[:arrow_heading_up: Back to TOP](#toc)

