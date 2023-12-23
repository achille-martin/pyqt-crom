# Simple PyQt Cross-Platform App

<a id="purpose"></a>

:dart: Create cross-platform apps (Android and Linux) using only Python and the Qt Framework (PyQt5). 

<a href="https://www.buymeacoffee.com/achille_martin" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png" alt="Buy Me A Coffee" width="200px"></a>

<a href="https://github.com/sponsors/achille-martin" target="_blank"><img src="https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&link=%3Curl%3E&color=f88379" width="200px"></a>

<a id="toc"></a>
## Table of Contents

* [1. Getting started](#getting-started)
    * [1.1. Check the pre-requisites](#pre-requisites)
    * [1.2. Setup the path to the main repo](#repo-path-setup)
    * [1.3. Download the github repo](#github-repo-download)
    * [1.4. Setup the virtual environment for the demo app](#virtual-environment-setup)
        * [1.4.1. Create a virtual environment with python3 installed on your machine](#virtual-environment-creation)
        * [1.4.2. Activate your virtual environment](#virtual-environment-activation)
        * [1.4.3. Install the necessary pip packages](#pip-package-installation)
        * [1.4.4. Test the PyQt5 demo app in your virtual environment](#virtual-environment-app-test)
    * [1.5. Install the external dependencies](#external-dependency-installation)
        * [1.5.1. Download a set of external dependencies for pyqtdeploy](#external-dependency-download)
        * [1.5.2. Install Java for Android Studio](#java-installation)
        * [1.5.3. Install Android Studio](#android-studio-installation)
        * [1.5.4. Install correct Android SDK and Tools](#android-sdk-installation)
        * [1.5.5. Install Android NDK matching with Qt version](#android-ndk-installation)
        * [1.5.6. Install Qt from the installer](#qt-installation)
    * [1.6. Setup the environment variables](#environment-variable-setup)
    * [1.7. Build the .apk with pyqtdeploy](#apk-build)
    * [1.8. Test the .apk](#apk-test)
* [2. Extra features for your Android app](#android-app-extra-features)
    * [2.1. Images](#pyqt5-images)
    * [2.2. File management](#pyqt5-file-management)
    * [2.3. Databases](#pyqt5-databases)
        * [2.3.1. Engine selection](#engine-selection)
        * [2.3.2. Setup for database management](#database-management-setup)
        * [2.3.3. Example PyQt5 app](#database-pyqt5-demo-app)
        * [2.3.4. Example operational PyQt5 app](#operational-database-pyqt5-demo-app)
    * [2.4. Graphics](#pyqt5-graphics)
        * [2.4.1. 2D Graphics](#pyqt5-2d-graphics)
        * [2.4.2. Example PyQt5 app](#graphics-pyqt5-demo-app)
        * [2.4.3. Example operational PyQt5 app](#operational-graphics-pyqt5-demo-app)
* [3. Generating your own app](#custom-app)
    * [3.1. Create your python package](#package-creation)
    * [3.2. Update the sysroot](#sysroot-update)
    * [3.3. Configure the pdy](#pdy-configuration)
    * [3.4. Build the apk](#app-generation)
    * [3.5. Debug the apk](#app-debugging)
* [4. How it all began...](#original-story)
    * [4.1. A fresh start](#fresh-start)
    * [4.2. Get the build files for pyqtdeploy](#original-build-files)
    * [4.3. Setup an app folder to build an .apk with pyqtdeploy](#original-setup)
    * [4.4. Setup, build and test the app](#original-build)
* [5. Troubleshooting](#troubleshooting)
    * [5.1. Module not found](#module-not-found)
    * [5.2. File not found](#file-not-found)
    * [5.3. Setup repo with VirtualBox](#virtualbox-setup)
* [6. Roadmap](#roadmap)
* [7. Credits](#credits)

<a id="getting-started"></a>
## 1. Getting started 

:mag: This section guides you through the process of generating a cross-platform app from a simple PyQt5 demo app.

<a id="pre-requisites"></a>
### 1.1. Check the pre-requisites 

Specs of Linux machine used:

- `Ubuntu 18.04` (EOL April 2028)

:bulb: _Refer to [Virtualbox Setup](#virtualbox-setup) if you don't have a Linux OS available on your machine._

- `Python 3.7.5` (EOL June 2023) and `pip3.7 (v23.3.1)`

`Ubuntu 18.04` is shipped with python 3.6.9, but `python 3.7.5` and `pip3.7` can be installed using:

```
sudo apt-get update \
&& sudo apt install python3.7 \
&& sudo apt install python3.7-dev \
&& sudo apt install curl \
&& cd $HOME \
&& curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
&& python3.7 get-pip.py \
&& python3.7 -m pip install --upgrade pip
```

Then, update your `$HOME/.bashrc` for easier python/pip access:

```
printf "%s\n" \
"" \
"# Ensuring stable python version" \
"alias python3=python3.7" \
"alias pip3='python3.7 -m pip'" \
"" \
>> $HOME/.bashrc \
&& source $HOME/.bashrc

```

:bulb: _Dev options for `python3.7` are required by PyQt5-sip (Python.h)._

Specs of target OS:

- `Android 9.0` (app can be used with later Android versions but won't pack the latest Android features)

<a id="repo-path-setup"></a>
### 1.2. Setup the path to the main repo

:warning: _We will use `SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR` as the variable containing the path to the main repo._

Add the variable to your `.bashrc` with:

```
printf "%s\n" \
"" \
"# Environment variable for Simple PyQt Cross-Platform App path" \
"export SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR=$HOME/Documents/simple-pyqt-cross-platform-app" \
"" \
>> $HOME/.bashrc \
&& source $HOME/.bashrc
```

<a id="github-repo-download"></a>
### 1.3. Download the github repo 

```
cd $HOME/Documents \
&& git clone git@github.com:achille-martin/simple-pyqt-cross-platform-app
```

<a id="virtual-environment-setup"></a>
### 1.4. Setup the virtual environment for the demo app 

<a id="virtual-environment-creation"></a>
#### 1.4.1. Create a virtual environment with python3 installed on your machine

```
pip3 install virtualenv \
&& cd $SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR \
&& mkdir -p venv \
&& cd venv \
&& virtualenv simple-pyqt-cross-platform-app-venv -p python3.7 \
&& cd ..
```

<a id="virtual-environment-activation"></a>
#### 1.4.2. Activate your virtual environment

```
source $SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR/venv/simple-pyqt-cross-platform-app-venv/bin/activate
```

:bulb: _To exit the virtual environment, type in your terminal `deactivate`._

<a id="pip-package-installation"></a>
#### 1.4.3. Install the necessary pip packages

```
cd $SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR \
&& pip3 cache purge \
&& pip3 install -r requirements.txt
```

:bulb: _You can confirm the installed pip packages with `pip3 list --local`._

<a id="virtual-environment-app-test"></a>
#### 1.4.4. Test the PyQt5 demo app in your virtual environment

```
cd $SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR/examples/demo/demo_pkg \
&& python3 demo_pyqt5_app.py
```

The PyQt5 demo app will start and you can confirm that it is displayed properly on your machine:
- Click the button
- An alert message is displayed stating that you have clicked the button

<a id="external-dependency-installation"></a>
### 1.5. Install the external dependencies

<a id="external-dependency-download"></a>
#### 1.5.1. Download a set of external dependencies for pyqtdeploy

Download the sources with:

```
cd $SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR/utils/resources \
&& chmod +x download_sources.sh \
&& ./download_sources.sh
```

:bulb: _You can confirm that the list of packages required matches with the versions from `$SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR/utils/sysroot.toml`._

<a id="java-installation"></a>
#### 1.5.2. Install Java for Android Studio

Install a stable java jdk available for your Ubuntu distribution and tested with Gradle:

```
sudo apt install openjdk-8-jdk openjdk-8-jre
```

Set the default java and javac version to 8 using:

```
sudo update-alternatives --config java \
&& sudo update-alternatives --config javac
```

:hand: *Confirm the version with `java -version && javac -version` which should be `v1.8.0_362`.*

<a id="android-studio-installation"></a>
#### 1.5.3. Install Android Studio

Download Android Studio (latest version) from [the Android studio website](https://developer.android.com/studio) or get the version `2022.3.1.22` used for this repo:

```
cd $HOME/Downloads \
&& wget https://redirector.gvt1.com/edgedl/android/studio/ide-zips/2022.3.1.22/android-studio-2022.3.1.22-linux.tar.gz
```

Move the contents of the downloaded `tar.gz` to your `$HOME` directory using:

```
cd $HOME/Downloads \
&& tar -xvf android-studio-2022.3.1.22-linux.tar.gz \
&& mv android-studio $HOME
```

Start the installation with:

```
cd $HOME/android-studio/bin \
&& ./studio.sh
```

_Tip: if there is an issue with android studio start, use `sudo ./studio.sh`._

The Android Studio installer will start:
- Do not import settings
- Select custom installation if possible
- Deselect Virtual Device if you don't need it for testing
- Keep a note of the Sdk installation path, which should be `$HOME/Android/Sdk`
- Start the download (unless you want to install extra features)

:hand: _Make sure that the default SDK has been installed in `$HOME/Android/Sdk` and that `$HOME/Android/Sdk/platforms` contains `android-28` folder only.
The reason why android-28 (corresponding to Android v9.0) is selected is because there are restrictions depending on the Java version installed.
If not, follow the instructions at the next step to set things up correctly._

<a id="android-sdk-installation"></a>
#### 1.5.4. Install correct Android SDK and Tools

- Restart Android Studio with `cd $HOME/android-studio/bin && ./studio.sh` (skip / cancel if no SDK found)
- On the menu screen, click on `more options` and then `SDK manager`
    - Make sure that you are in the Settings -> Languages & Frameworks -> Android SDK
    - Make sure that in the `SDK Platforms` tab, the following is installed: (Android 9.0) Android SDK Platform 28, (Android 9.0) Sources for Android 28.
    - Remove any additional unneeded package from the list.
    - Apply changes for `SDK Platforms` tab.
    - Make sure that in the `SDK Tools` tab, the following is installed (you need to untick Hide Obsolete Packages and tick Show Package Details): (Android SDK Build-Tools 34) v28.0.3, Android Emulator any version, Android SDK Tools (Obsolete) v26.1.1. Uninstall any other interfering package.
- Close Android Studio
- Download SDK Platform-Tools v28.0.3 to match the SDK Build-Tools version and add it to your SDK folder using:

```
cd $HOME/Downloads \
&& wget https://dl.google.com/android/repository/platform-tools_r28.0.3-linux.zip \
&& sudo apt-get install unzip \
&& unzip platform-tools_r28.0.3-linux.zip \
&& rm -r $HOME/Android/Sdk/platform-tools \
&& mv platform-tools $HOME/Android/Sdk
```

<a id="android-ndk-installation"></a>
#### 1.5.5. Install Android NDK working with Qt version

- Restart Android Studio with `cd $HOME/android-studio/bin && ./studio.sh` (skip / cancel if no SDK found)
- On the menu screen, click on `more options` and then `SDK manager`
    - Make sure that you are in the Settings -> Languages & Frameworks -> Android SDK
    - Make sure that in the `SDK Tools` tab, the following is installed as an additional package to the previous ones: NDK Side-By-Side v21.4.7075529 (equivalent to r21e). According to the [Qt Website](https://doc.qt.io/qt-5/android-getting-started.html), this is the one recommended for Qt5.15.2.
- Close Android Studio

:hand: _Make sure that `$HOME/Android/Sdk/ndk/21.4.7075529/platforms` contains the folder `android-28`._

:bulb: _The NDK corresponds to the minimum version required to run the app. Technically, you could choose a lower version._

<a id="qt-installation"></a>
#### 1.5.6. Install Qt from the installer

Download the Qt version which matches the one in `$SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR/utils/sysroot.toml` from the open source online installer:

```
sudo apt-get install wget \
&& sudo apt-get install libxcb-xfixes0-dev \
&& cd $HOME/Downloads \
&& wget https://d13lb3tujbc8s0.cloudfront.net/onlineinstallers/qt-unified-linux-x64-4.6.1-online.run \
&& chmod +x qt*.run \
&& ./qt-unified-linux-x64-4.6.1-online.run
```

A Qt window will appear on which you can sign up:
- Verify your email and register as an individual (no need for location)
- Restart the Qt installer with: `cd $HOME/Downloads && ./qt-unified-linux-x64-4.6.1-online.run`
- Log in, state that you are an individual and not a company
- Setup will start
- Select folder location `$HOME/Qt5.15.2`
- Installation will start

:bulb: _If custom installation has to be selected, make sure you only setup `Qt5.15.2` and the default packages._

:hand: _Make sure that you can access `$HOME/Qt5.12.2/5.12.2` and that the folder `android` is located inside of it._

<a id="environment-variable-setup"></a>
### 1.6. Setup the environment variables

Load the environment variables on terminal startup with:

```
printf "%s\n" \
"" \
"# Load extra environment variables for Simple PyQt Cross-Platform App" \
"source $SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR/utils/resources/path_setup.sh" \
"" \
>> $HOME/.bashrc \
&& source $HOME/.bashrc
```

<a id="apk-build"></a>
### 1.7. Build the .apk with pyqtdeploy

Start the building process of the .apk with:

```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app
python3 build_app.py --target android-64 --source-dir $RESOURCES_DIR --installed-qt-dir $QT_DIR --verbose
``` 
:hourglass_flowing_sand: _Let the app build (it may take a while)._

:tada: _The app is built when you see "BUILD SUCCESSFUL"._

:bulb: _The next time you build an app, you can skip the creation of the sysroot._
_Use the following command for future builds:_

```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app
python3 build_app.py --target android-64 --source-dir $RESOURCES_DIR --installed-qt-dir $QT_DIR --verbose --no-sysroot
```

_Note: the Android Manifest can be checked at debug stage at `build-android-64/android-build/build/intermediates/packaged_manifests/debug/AndroidManifest.xml`._

_Note2: the `build.gradle` file located in `build-android-64/android-build` gives crucial information on min and max versions of components._

<a id="apk-test"></a>
### 1.8. Test the .apk 

The generated `example_pyqt5_app-debug.apk` can be found in `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/build-android-64/example_pyqt5_app/build/outputs/apk/debug`.

You can then either:
- Copy, install and run the .apk onto your phone (>=Android v9.0)
- Install BlueStacks on Windows (https://www.bluestacks.com/download.html), enable hyper-V, open `my games` and install the .apk, run the app offline

[:arrow_heading_up: Back to TOP](#toc) 

<a id="android-app-extra-features"></a>
## 2. Extra features for your Android app

:mag: This section introduces a few outstanding capabilities of PyQt5 which can be ported to your Android app.

The demo app only contains a very small set of PyQt5 features, but this section explores the full potential of PyQt5 and gives hints on how to make a fully working Android (prototype) app.

<a id="pyqt5-images"></a>
### 2.1. Images

Use `QPixmap` and `pyrcc` to save images and render them.

<a id="pyqt5-file-management"></a>
### 2.2. File management

Rely on python modules to create a structured project folder with writable paths.

<a id="pyqt5-databases"></a>
### 2.3. Databases

<a id="engine-selection"></a>
#### 2.3.1. Engine selection

The preferred database engine for Android is `SQLite`. The latest SQLite library available is `sqlite3` as introduced on [the SQLite website](https://www.sqlite.org/version3.html).

PyQt5 lets you work with many other database engines as shown on [tutorialspoint website](https://www.tutorialspoint.com/pyqt5/pyqt5_database_handling.htm), but `sqlite3` is a good start for simple python apps because:
- The application file is portable across multiple platforms
- Reading/writing performance is great as the application only loads the data it needs
- Content is updated continuously and atomically for maximum reliability
- Database content can be viewed with many third-party tools

<a id="database-management-setup"></a>
#### 2.3.2. Setup for database management

Before attempting to run any `SQLite`-related actions, make sure that the library is available on your machine:

```
sudo apt-get install sqlite3
sudo apt-get install sqlitebrowser
```

<a id="database-pyqt5-demo-app"></a>
#### 2.3.3. Example PyQt5 app

To confirm that `SQLite` is functional on your machine, run the following:

```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqt_feature_testing/database
python3 pyqt5_app_with_database.py
```

A dialog window will pop up in which you can perform the following:
- View the pre-populated database (called `sportsdatabase.db`)
- Add a row to the database
- Remove a row from the database

You can view the content of the generated and edited database at any time outside of the application with:

```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqt_feature_testing/database
sqlitebrowser sportsdatabase.db
```

<a id="operational-database-pyqt5-demo-app"></a>
#### 2.3.4. Example operational PyQt5 app

You can also run a more operational PyQt5 app boasting a database with:

```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqt_feature_testing/database
python3 operational_pyqt5_app_with_database.py
```

This demo app is built on the one highlighted in the [Getting started](#getting-started) section:
- A window appears on the screen in a window with 2 buttons: MAGIC or EXIT
- Once MAGIC is clicked, a pop-up appears on screen stating that the button has been clicked and that a database will open
- Once the pop-up has been acknowledged, a database (called `sportsdatabase.db`) is created in the `home` folder as shown in the alert window, if not already existing
- In the dialog window displaying the content of the database, rows can be added, removed or edited

:point_up: _You can view the content of `sportsdatabase.db` at any time by following the instructions in [Example PyQt5 app with database](#database-pyqt5-demo-app) after ensuring that your [Database manager](#database-management-setup) is correctly setup._

<a id="pyqt5-graphics"></a>
### 2.4. Graphics

<a id="pyqt5-2d-graphics"></a>
#### 2.4.1. 2D Graphics

There are 2 main approaches to create 2D Graphics in Qt apps:
* QGraphics way
* QtQuick way

QGraphics relies on a database of useful shapes and widgets (QWidgets) to make the app efficient and native (the look is tied to the platform). As described on the [pythonguis website](https://www.pythonguis.com/tutorials/pyqt-qgraphics-vector-graphics/), QGraphics harnesses the model-view paradigm through QGraphicsScene (model), QGraphicsView (view) and QGraphicsItems (visual elements).

QtQuick on the other hand, relies on the Qt Modeling language (QML) to define user interfaces. As described on the [pythonguis website](https://www.pythonguis.com/tutorials/qml-qtquick-python-application/), QML is focused on custom UI design and is useful for consistent app design across multiple platforms. The look of the app will be more modern, but the development might take longer.

As we are showcasing a prototyping tool for mobile apps, we have decided to explore QGraphics options rather than follow QtQuick practices. Note that both approaches are viable and handled by the pyqtdeploy tool.

<a id="graphics-pyqt5-demo-app"></a>
#### 2.4.2. Example PyQt5 app

To visualise a basic example of 2D Graphics in a PyQt app, run the following:


```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqt_feature_testing/graphics
python3 pyqt5_app_with_graphics.py
```

A graphics window will appear, in which you can perform the following:

* Move shapes around and locate their centre thanks to the status bar prompt
* Get back to the home screen thanks to the button at the top of the window

<a id="operational-graphics-pyqt5-demo-app"></a>
#### 2.4.3. Example operational PyQt5 app

You can also run a more operational PyQt5 app boasting a graphics playground with:

```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqt_feature_testing/graphics
python3 operational_pyqt5_app_with_graphics.py
```

This demo app is built on the one highlighted in the [Getting started](#getting-started) section:
- A window appears on the screen in a window with 2 buttons: MAGIC or EXIT
- Once MAGIC is clicked, a pop-up appears on screen stating that the button has been clicked and that a graphics playground will open
- Once the pop-up has been acknowledged, a graphics playground opens up with 2 shapes that can be dragged around
- When selecting a shape, its coordinates are displayed at the bottom of the screen, in the status bar
- To exit the graphics playground, hit the HOME button

[:arrow_heading_up: Back to TOP](#toc) 

<a id="custom-app"></a>
## 3. Generating your own app

_This section describes the step to generate your own `.apk` from a `PyQt5` app._

<a id="package-creation"></a>
### 3.1. Create your python package

Start by creating a python package to hold your `PyQt5` app:
* Create a folder `<pkg_name>`
* Populate with at least `__init__.py` file and a `<app_name>.py` script

_Note that the `<app_name>.py` must contain a unique `main()` function (or any similar distinctive entry point)._

* Add more files if required for your package

<a id="sysroot-update"></a>
### 3.2. Update the sysroot

Make sure that you update the `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/sysroot.json` with any new module.

For instance, if you imported `QtSql` in your `PyQt5` app, then you must include `QtSql` in the `pyqt5/android#modules`.

<a id="pdy-configuration"></a>
### 3.3. Configure the pdy

Follow up by configuring the `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/config_app.pdy` file:

APPLICATION SOURCE TAB
* Open the `.pdy` file with `cd $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app && pyqtdeploy config_app.pdy`
* Define an application name (called <apk_name>) with no spaces
* Define an entry point in the form `<pkg_name>.<app_name>:main`
* Add `sys.path` if necessary
* Scan for the application package directory <pkg_name> and tick the files/subfolders you want to include in the apk
* Confirm the python and PyQt versions

PYQT MODULES TAB
* Tick all relevant Qt modules required for your app

STANDARD LIBRARY TAB
* Tick all python libraries required for your app

REMAINING TABS
* Leave as it is or add elements as necessary

Once you have updated the `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/config_app.pdy`, you can save it.

<a id="app-generation"></a>
### 3.4. Build the apk

Follow up with the building of your app.

Generate the `<apk_name>.apk` located in the `<pkg_name>/releases/<date>` repo with:

```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app
python3 build_app.py --target android-64 --source-dir $RESOURCES_DIR --installed-qt-dir $QT_DIR --verbose --no-sysroot
```

:hand: _If it is your first time using `build_app.py`, please refer to the [build instructions](#apk-build)._

<a id="app-debugging"></a>
### 3.5. Debug the apk

The most nerve-wracking part of deploying an application is the debugging part. 
Therefore, make sure that you have added a logger to your application and that you use an Emulator (or a physical device) to confirm your expectations.

To setup an Android Emulator, it is recommended to use Android Studio.

_If you want to set up the Android Emulator in VirtualBox, please refer to [this issue](https://github.com/achille-martin/simple-pyqt5-android-app/issues/12)._

To setup the Android Emulator in Ubuntu, make sure that you have:
* Android Studio installed (refer to [External dependencies setup](#external-dependency-installation) if needed)
* Correctly set up Android Studio as per [Expo dev recommendations](https://docs.expo.dev/workflow/android-studio-emulator/)
* Added the following to your `$HOME/.bashrc`

```
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

* Have correctly set up the virtualisation solution and solved potential issues mentioned on [Stackoverflow](https://stackoverflow.com/questions/37300811/android-studio-dev-kvm-device-permission-denied)

```
sudo apt install qemu-kvm
ls -al /dev/kvm
sudo adduser <username> kvm
sudo chown <username> /dev/kvm
```

Once the Android Emulator is set up and running, you can drag and drop your `.apk` to install it and run it.

If you wish to access more Android logs, please refer to [this issue](https://github.com/achille-martin/simple-pyqt5-android-app/issues/12), which mentions tips for `adb`, the Android Debug Bridge.

[:arrow_heading_up: Back to TOP](#toc)

<a id="original-story"></a>
## 4. How it all began...

:mag: This section shows you how this repo came to life by leveraging the functionalities of [pyqtdeploy](https://pypi.org/project/pyqtdeploy/).

<a id="fresh-start"></a>
### 4.1. A fresh start

Get rid of `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app` folder:

```
sudo rm -r $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app
```

<a id="original-build-files"></a>
### 4.2. Get the build files for pyqtdeploy

- Download the `pyqt-demo` folder from [pypi website](https://pypi.org/project/pyqtdeploy/2.5.1/#files) or use the following command:

```
cd $HOME/Downloads
wget https://files.pythonhosted.org/packages/ea/7e/2ac107e713badfbb6ae6ac6f2272a78f060e846748bcb83e7c71413badc9/pyqtdeploy-2.5.1.tar.gz 
```

:warning: _Stick to v2.x as v3.x had some major changes which will generate loads of issues._

:hand: _Make sure that you get the matching `pyqtdeploy` version you installed with `pip`_

- Extract the contents of the `.tar.gz` into `$SIMPLE_PYQT5_ANDROID_APP_DIR` with the command:

```
cd $HOME/Downloads
tar -xvf pyqtdeploy-2.5.1.tar.gz
mv pyqtdeploy-2.5.1/ $SIMPLE_PYQT5_ANDROID_APP_DIR
```

:hand: *Make sure that you now have a folder called `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-2.5.1`*

<a id="original-setup"></a>
### 4.3. Setup an app folder to build an .apk with pyqtdeploy

- Create a new folder called `pyqtdeploy_app`:

```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR
mkdir pyqtdeploy_app
```

- Copy the contents of `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy-2.5.1/demo` into `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app`:
- Delete `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/pyqt-demo.py`
- Rename `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/build-demo.py` into `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/build_app.py`
- Replace the line `shutil.copy('pyqt-demo.py', os.path.join('data', 'pyqt-demo.py.dat'))` in `build_app.py` with:

```
shutil.copy('../example_pyqt5_app.py', os.path.join('data', 'example_pyqt5_app.py.dat'))
```

- Rename all occurrences of `pyqt-demo` into `example_pyqt5_app` in `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/build_app.py`
- Rename `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/pyqt-demo.pdy` into `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/example_pyqt5_app.pdy`
- Update the `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/example_pyqt5_app.pdy` with the necessary packages:

```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app
pyqtdeploy example_pyqt5_app.pdy
```

- Update the location of the main script file in `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/example_pyqt5_app.pdy`: use the file explorer to find `example_pyqt5_app.py`
- Rename `pyqt-demo.py.dat` inside of `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/example_pyqt5_app.pdy` with vim into: `example_pyqt5_app.py.dat`
- Check your python version (in your virtual environment) and make the version in `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/example_pyqt5_app.pdy` match: select the right one
- In the PyQt Modules tab of `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/example_pyqt5_app.pdy`, select your relevant Qt modules. For instance: QtCore, QtWidgets.

:point_up: _The `.pdy` might force include some default Qt modules like: `QtGui`, `sip`._

- In the Standard Library tab of `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/example_pyqt5_app.pdy`, remove all the extra modules and keep only the default ones. If needed for your app, add more.
- Update `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/sysroot.json` to reflect the packages selected in `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/example_pyqt5_app.pdy` and the desired versions
- Remove the following packages (for the example) from `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/sysroot.json`: openssl, zlib, pyqt3d, pyqtchart, pyqtdatavisualization, pyqtpurchasing, qscintilla
- Keep the following packages (for the example) in `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/sysroot.json`: qt5 version 5.12.2, python update to version 3.6.9 (the version in your virtual environment), sip version 4.19.15, pyqt5 version 5.12.1 (even though v.5.15.6 installed in virtual environment)
- in PyQt5 section of `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/sysroot.json`, update the list of android modules to match `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/example_pyqt5_app.pdy`:

```
        "android#modules":              [
                "QtCore", "QtGui", "QtWidgets"
        ],
```

<a id="original-build"></a>
### 4.4. Setup, build and test the app

Please follow the steps detailed in [Getting Started](#getting-started) to setup, build and test your own PyQt5 app.

If you would like to understand how `pyqtdeploy` works and how to set it up, please refer to the [official tutorial](https://docs.huihoo.com/pyqt/pyqtdeploy/tutorial.html).

[:arrow_heading_up: Back to TOP](#toc) 

<a id="troubleshooting"></a>
## 5. Troubleshooting

:mag: This section walks you through tips and fixes for the main challenges you might encounter.

<a id="module-not-found"></a>
### 5.1. Module not found

When trying to run the PyQt5 app on your machine, the following issue might come up:

```
Traceback (most recent call last):
  File "./example_pyqt5_app.py", line 8, in <module>
    from PyQt5.QtCore import QSize
ModuleNotFoundError: No module named 'PyQt5'
```

This means that the python modules have not been correctly loaded.

Please make sure that you have followed the [Getting started](#getting-started) tutorial.
If you have followed the tutorial, then ensure that you have [activated your virtual environment](#virtual-environment-activation).

<a id="file-not-found"></a>
### 5.2. File not found

If the [building process](#apk-build) or any other process fails because some files cannot be found, ensure that you have correctly setup your `.bashrc` to load the environment.

Go through the [Getting started](#getting-started) tutorial and confirm the state of your `.bashrc`.

<a id="virtualbox-setup"></a>
### 5.3. Setup repo with VirtualBox

To setup a Linux Virtual Machine on Windows via VirtualBox, follow [It's FOSS virtualbox setup tutorial](https://itsfoss.com/install-linux-in-virtualbox/).
If you would prefer to setup a Linux Virtual Machine on MacOS via VirtualBox, follow [TecAdmin virtualbox setup tutorial](https://tecadmin.net/how-to-install-virtualbox-on-macos/).

It is also recommended to install the VirtualBox Guest Additions. Follow the [LinuxTechi guest addition setup tutorial](https://www.linuxtechi.com/install-virtualbox-guest-additions-on-ubuntu/) for more information.

When setting the repo up in VirtualBox and trying to install Qt, you might come across the following issue with `xcb`:

```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
```

- First, enable the Qt debug prints:

```
export QT_DEBUG_PLUGINS=1
```

- Second, identify the issue:

    - If it is related to the package `libxcb-xinerama`, then download the package with:

```
sudo apt-get install libxcb-xinerama0
``` 

[:arrow_heading_up: Back to TOP](#toc) 

<a id="roadmap"></a>
## 6. Roadmap

_This section describes the broad roadmap to deliver a functional repo._

![Roadmap Diagram](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/achille-martin/simple-pyqt-cross-platform-app/master/doc/roadmap/roadmap.iuml)

[:arrow_heading_up: Back to TOP](#toc) 

<a id="credits"></a>
## 7. Credits

Repository created and maintained by [Achille Martin](https://github.com/achille-martin).

:money_with_wings: Donations are welcomed as hard work has been put into this repository.

If you feel you can make progress with your projects by converting your PyQt5 apps into Android apps, please support this project.

:warning: _This repo is aimed at boosting the capability of well-intentioned international developers to create apps benefitting the community._

Inspiration for this repo comes from:
- [Kviktor's github repo](https://github.com/kviktor/pyqtdeploy-android-build)
- [Lola Rigaut-Luczak's medium article](https://medium.com/@Lola_Dam/packaging-pyqt-application-using-pyqtdeploy-for-both-linux-and-android-32ac7824708b)

Huge thanks to [Phil Thompson](https://pypi.org/user/PhilThompson/), the creator and maintainer of [PyQt](https://riverbankcomputing.com/software/pyqt/intro) and [pyqtdeploy](https://pypi.org/project/pyqtdeploy/).

[:arrow_heading_up: Back to TOP](#toc)

