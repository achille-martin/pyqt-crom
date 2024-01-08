# Simple PyQt Cross-Platform App

<a id="purpose"></a>

:dart: Create cross-platform apps (Android) using only Python and the Qt Framework (PyQt5). 

<a href="https://www.buymeacoffee.com/achille_martin" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png" alt="Buy Me A Coffee" width="200px"></a>

<a href="https://github.com/sponsors/achille-martin" target="_blank"><img src="https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&link=%3Curl%3E&color=f88379" width="200px"></a>

<a id="toc"></a>
## Table of Contents

* [1. Getting started](#getting-started)
    * [1.1. Check the pre-requisites](#pre-requisites)
    * [1.2. Download the github repo](#github-repo-download)
    * [1.3. Setup the path to the main repo](#repo-path-setup)
    * [1.4. Setup the python virtual environment](#virtual-environment-setup)
        * [1.4.1. Create a virtual environment with python installed on your machine](#virtual-environment-creation)
        * [1.4.2. Activate your virtual environment](#virtual-environment-activation)
        * [1.4.3. Install the necessary pip packages](#pip-package-installation)
        * [1.4.4. Test the PyQt5 demo app in your virtual environment](#virtual-environment-app-test)
    * [1.5. Install the external dependencies](#external-dependency-installation)
        * [1.5.1. Download a set of external dependencies for pyqtdeploy](#external-dependency-download)
        * [1.5.2. Install Zlib for pyqtdeploy](#zlib-installation)
        * [1.5.3. Install Java for Android Studio](#java-installation)
        * [1.5.4. Install Android Studio](#android-studio-installation)
        * [1.5.5. Install correct Android SDK and Tools](#android-sdk-installation)
        * [1.5.6. Install Android NDK matching with Qt version](#android-ndk-installation)
        * [1.5.7. Install Qt from the installer](#qt-installation)
    * [1.6. Setup the environment variables](#environment-variable-setup)
    * [1.7. Build the app with pyqtdeploy](#app-build)
    * [1.8. Test the app](#app-test)
* [2. Generating your own app](#custom-app)
    * [2.1. Create your python package](#package-creation)
    * [2.2. Update the sysroot](#sysroot-update)
    * [2.3. Configure the pdt](#pdt-configuration)
    * [2.4. Build the app](#app-generation)
    * [2.5. Debug the app](#app-debugging)
* [3. Extra features for your app](#app-extra-features)
* [4. Troubleshooting](#troubleshooting)
* [5. Roadmap](#roadmap)
* [6. Credits](#credits)

<a id="getting-started"></a>
## 1. Getting started 

:mag: This tutorial guides you through the process of generating a cross-platform app from a simple PyQt5 demo app.

:trophy: By the end of the tutorial, you will be able to launch the simple PyQt5 demo app from your Android phone:

<a id="pyqt5-demo-app-android-video"></a>

<video src="https://github.com/achille-martin/simple-pyqt-cross-platform-app/assets/66834162/6724ea92-18ee-4471-82a8-2bf255765506">
   <p>PyQt5 demo app Android platform video</p>
</video>

<a id="pre-requisites"></a>
### 1.1. Check the pre-requisites 

Specs of Linux machine used:

- `Ubuntu 22.04` (EOL April 2032)
- `Python 3.10.12` (EOL October 2026) and `pip3 v23.3.2`

:bulb: _Refer to [Virtual Machine Setup](#virtual-machine-setup) if you don't have a Linux OS available on your machine._

:bulb: _Setup pip3 on Ubuntu with:_

```
sudo apt-get update
sudo apt-get install python3-pip
python3 -m pip install --upgrade pip
```

Specs of target OS:

- `Android 9.0` as targeted Android features (default)
- `Android 9.0` as minimum Android version to run the app (default)

<a id="github-repo-download"></a>
### 1.2. Download the github repo 

```
cd $HOME/Documents \
&& git clone git@github.com:achille-martin/simple-pyqt-cross-platform-app
```

<a id="repo-path-setup"></a>
### 1.3. Setup the path to the main repo

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

<a id="virtual-environment-setup"></a>
### 1.4. Setup the python virtual environment

<a id="virtual-environment-creation"></a>
#### 1.4.1. Create a virtual environment with python3 installed on your machine

```
sudo apt-get install python3-virtualenv \
&& cd $SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR \
&& mkdir -p venv \
&& cd venv \
&& virtualenv simple-pyqt-cross-platform-app-venv -p python3 \
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

Upgrade your version of pip to v23.3.2 in the virtual environment with:

```
pip3 install --upgrade pip
```

Install the pip packages with:

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

<video src="https://github.com/achille-martin/simple-pyqt-cross-platform-app/assets/66834162/250e9449-bcde-437c-8cfd-2c4b71514736">
   <p>PyQt5 demo app Linux platform video</p>
</video>

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

<a id="zlib-installation"></a>
#### 1.5.2. Install Zlib for pyqtdeploy

Install zlib on Ubuntu with:

```
sudo apt install zlib1g-dev
```

Zlib is required by the pyqtdeploy project `$SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR/utils/pyqt-demo.pdt` to correctly identify the dependencies from the `$SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR/utils/sysroot.toml`.

Sysroot setup tips can be obtained from [Riverbank website](https://www.riverbankcomputing.com/static/Docs/pyqtdeploy/sysroot.html).

<a id="java-installation"></a>
#### 1.5.3. Install Java for Android Studio

Install stable java JDK 11 available for your Ubuntu distribution and tested with Gradle:

```
sudo apt install openjdk-11-jdk openjdk-11-jre
```

Set the default java and javac version to 11 using:

```
sudo update-alternatives --config java \
&& sudo update-alternatives --config javac
```

:hand: _Confirm the version with `java -version && javac -version` which should be `v11.0.21`._

<a id="android-studio-installation"></a>
#### 1.5.4. Install Android Studio

Download Android Studio version `2023.1.1.26` with:

```
sudo apt-get install wget \
&& cd $HOME/Downloads \
&& wget https://redirector.gvt1.com/edgedl/android/studio/ide-zips/2023.1.1.26/android-studio-2023.1.1.26-linux.tar.gz
```

Move the contents of the downloaded `tar.gz` to your `$HOME` directory using:

```
cd $HOME/Downloads \
&& tar -xvf android-studio-2023.1.1.26-linux.tar.gz \
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
- Pick the default Android SDK
- Deselect Virtual Device if you don't need it for testing
- Keep a note of the Sdk installation path, which should be `$HOME/Android/Sdk`
- Start the download (unless you want to install extra features)
- Close Android Studio

:hand: _Make sure that the default SDK has been installed in `$HOME/Android/Sdk` and that `$HOME/Android/Sdk/platforms` contains `android-28` folder only.
The reason why android-28 (corresponding to Android v9.0) is selected is because there are restrictions depending on the Java version installed and the Qt version installed.
If not, follow the instructions at the next step to set things up correctly._

<a id="android-sdk-installation"></a>
#### 1.5.5. Install correct Android SDK and Tools

- Restart Android Studio with `cd $HOME/android-studio/bin && ./studio.sh` (skip / cancel if no SDK found)
- On the menu screen, click on `more actions` and then `SDK manager`
    - Make sure that you are in the Settings -> Languages & Frameworks -> Android SDK
    - Make sure that in the `SDK Platforms` tab, the following is installed (Show package details and unhide obsolete packages): (Android 9.0) Android SDK Platform 28 and Sources for Android 28.
    - Remove any additional unneeded package from the list.
    - Apply changes for `SDK Platforms` tab.
    - Make sure that in the `SDK Tools` tab, the following is installed (Show package details and unhide obsolete packages): (Android SDK Build-Tools 28) v28.0.3, Android Emulator any version, Android SDK Tools (Obsolete) v26.1.1.
    - Remove any additional unneeded and interfering package from the list.
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
#### 1.5.6. Install Android NDK working with Qt version

- Restart Android Studio with `cd $HOME/android-studio/bin && ./studio.sh` (skip / cancel if no SDK found)
- On the menu screen, click on `more actions` and then `SDK manager`
    - Make sure that you are in the Settings -> Languages & Frameworks -> Android SDK
    - Make sure that in the `SDK Tools` tab, the following is installed as an additional package to the previous ones: NDK Side-By-Side v21.4.7075529 (equivalent to r21e). According to the [Qt Website](https://doc.qt.io/qt-5/android-getting-started.html), this is the one recommended for Qt5.15.2.
- Close Android Studio

:hand: _Make sure that `$HOME/Android/Sdk/ndk/21.4.7075529/platforms` contains the folder `android-28`._

:bulb: _The NDK corresponds to the minimum version required to run the app. Technically, you could choose a lower version than Android API 9.0 (android-28)._

<a id="qt-installation"></a>
#### 1.5.7. Install Qt from the installer

Download the Qt version which matches the one in `$SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR/utils/sysroot.toml` from the open source online installer:

```
sudo apt-get install libxcb-xfixes0-dev \
&& cd $HOME/Downloads \
&& wget https://d13lb3tujbc8s0.cloudfront.net/onlineinstallers/qt-unified-linux-x64-4.6.1-online.run \
&& chmod +x qt*.run \
&& ./qt-unified-linux-x64-4.6.1-online.run
```

A Qt window will appear on which you can sign up:
- Verify your email and register as an individual (no need for location)
- Restart the Qt installer with: `cd $HOME/Downloads && ./qt-unified-linux-x64-4.6.1-online.run`
- Log in, state that you are an individual and not a company
- If possible, select "Custom installation" and make sure to only setup `Qt5.15.2` (and other packages you might want)
- Setup will start
- Select folder location `$HOME/Qt5.15.2`
- Installation will start

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

<a id="app-build"></a>
### 1.7. Build the app with pyqtdeploy

Start the building process of the .apk with:

```
cd $SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR/utils \
&& python3 build_app.py --pdt $SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR/examples/demo/demo_project/config.pdt --jobs 1 --target android-64 --qmake $QT_DIR/android/bin/qmake --verbose
``` 
:hourglass_flowing_sand: _Let the app build (it may take a while)._

_Note: The app is built when you see "BUILD SUCCESSFUL"._

_The Android Manifest, `build.gradle` and `gradle.properties` can be checked at debug stage at `build-android-64/android-build`._

<a id="app-test"></a>
### 1.8. Test the app 

The generated `DemoCrossPlatformApp.apk` can be found in `$SIMPLE_PYQT_CROSS_PLATFORM_APP_DIR/examples/demo/demo_project/releases`.

You can then either:
- Copy, install and run the .apk onto your phone (>=Android v9.0)
- Install BlueStacks on Windows (https://www.bluestacks.com/download.html), enable hyper-V, open `my games` and install the .apk, run the app offline
- Setup a virtual device in Android Studio and install the app on it to access debugging messages and application-related files

:trophy: Congratulations! You have completed the tutorial. You can view the [demo app running on an Android phone](#pyqt5-demo-app-android-video).

[:arrow_heading_up: Back to TOP](#toc) 

<a id="custom-app"></a>
## 2. Generating your own app

_This section describes the step to generate your own `.apk` from a `PyQt5` app._

<a id="package-creation"></a>
### 2.1. Create your python package

Start by creating a project folder:
* Create a folder `<project_name>`

Inside of the project folder, create a python package to hold your `PyQt5` app:
* Create a folder `<project_name>/<pkg_name>`
* Populate with at least `__init__.py` file and a `<app_name>.py` script

_Note that the `<app_name>.py` must contain a unique `main()` function (or any similar distinctive entry point)._

* Add more files if required for your package

Inside of the project folder, add a config folder to hold your configuration files:
* Create a folder `<project_name>/config`
* Populate with `<app_name_sysroot>.toml` and `<app_name_config>.pdt` files

<a id="sysroot-update"></a>
### 2.2. Update the sysroot

Make sure that you update the `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app/sysroot.json` with any new module.

For instance, if you imported `QtSql` in your `PyQt5` app, then you must include `QtSql` in the `pyqt5/android#modules`.

<a id="pdt-configuration"></a>
### 2.3. Configure the pdt

Tip for 3.3.0: you can add a sysroot specification file (or sysroot directory) to target the exact file from the .pdt.

For more information, read on [Riverbank website](https://www.riverbankcomputing.com/static/Docs/pyqtdeploy/pyqtdeploy.html).

Make sure that any module imported in your `<app_name>.py` (or any part of your python project), is ticked in the .pdt file.

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
### 2.4. Build the app

Follow up with the building of your app.

Generate the `<apk_name>.apk` located in the `<pkg_name>/releases/<date>` repo with:

```
cd $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app
python3 build_app.py --target android-64 --source-dir $RESOURCES_DIR --installed-qt-dir $QT_DIR --verbose --no-sysroot
```

:hand: _If it is your first time using `build_app.py`, please refer to the [build instructions](#apk-build)._

<a id="app-debugging"></a>
### 2.5. Debug the app

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

<a id="app-extra-features"></a>
## 3. Extra features for your app

Refer to [PyQt5 features](doc/features/pyqt5_features.md) for this section.

<a id="troubleshooting"></a>
## 4. Troubleshooting

Refer to [Common issues](doc/troubleshooting/common_issues.md) for this section.

<a id="roadmap"></a>
## 5. Roadmap

:mag: This section describes the broad roadmap to deliver a functional repo.

![Roadmap Diagram](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/achille-martin/simple-pyqt-cross-platform-app/master/doc/roadmap/roadmap.iuml)

[:arrow_heading_up: Back to TOP](#toc) 

<a id="credits"></a>
## 6. Credits

Repository created and maintained by [Achille Martin](https://github.com/achille-martin).

If you feel you can make progress with your projects by converting your PyQt5 apps into cross-platform apps, please support this project.

<a href="https://www.buymeacoffee.com/achille_martin" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png" alt="Buy Me A Coffee" width="200px"></a>

<a href="https://github.com/sponsors/achille-martin" target="_blank"><img src="https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&link=%3Curl%3E&color=f88379" width="200px"></a>

:warning: _This repo is aimed at boosting the capability of well-intentioned international developers to create apps benefitting the community._

:clap: Huge thanks to [Phil Thompson](https://pypi.org/user/PhilThompson/), the creator and maintainer of [PyQt](https://riverbankcomputing.com/software/pyqt/intro) and [pyqtdeploy](https://pypi.org/project/pyqtdeploy/).

[:arrow_heading_up: Back to TOP](#toc)

