# simple-pyqt5-android-app

## Purpose 

_This section explains the purpose of the repo._

The aim is to create an android app (.apk) from a simple PyQt5 app.

## Example App Demo

_This section explains the process to generate an .apk for a simple pyqt5 demo app._

### Pre-requisites

Specs of Linux machine used:
* Ubuntu 18.04
* Python 3.6.9

Target:
* Android 9.0 (at least)

### Download the github repo

```
cd ~/Documents
git clone git@github.com:achille-martin/simple-pyqt5-android-app.git
```

*Note that we will use `$APP_DIR` as the path to your own app folder*

```
export APP_DIR=~/Documents/simple-pyqt5-android-app
```

### Setup the virtual environment for your app

1) Create a virtual environment with your python3 installed on your computer

```
cd $APP_DIR
pip3 install virtualenv
mkdir venv
cd venv
virtualenv simple-pyqt5-android-app-venv -p python3
```

2) Activate your virtual environment

```
source $APP_DIR/venv/simple-pyqt5-android-app-venv/bin/activate
```

_Note: to exit, type in a terminal `deactivate`_

3) Install the necessary pip packages

```
cd $APP_DIR
pip3 cache purge
pip3 install -r requirements.txt
```

_Note that `pip --version` should display a version related to python 3.x_

Confirm your pip packages with:

```
pip3 list --local
```

4) Test your virtual environment

```
cd $APP_DIR
python example-pyqt5-app.py
```

Confirm that your pyqt5 app can be displayed properly in Linux:
- Click a button
- An alert message is displayed stating that you have clicked the button

### Install the external dependencies and setup the environment variables

1) Download a set of external dependencies

A folder has been created to hold the resources (with the desired versions): `$APP_DIR/pyqtdeploy-app/resources`.

A file called `download_sources.sh` has been added to `$APP_DIR/pyqtdeploy-app/resources` to gather all resources at once.
Please download the sources:
```
cd $APP_DIR/pyqtdeploy-app/resources
chmod +x download_sources.sh
./download_sources.sh
```

_Note: you can confirm that the list of packages required matches with the versions from `$APP_DIR/pyqtdeploy-app/sysroot.json`_

2) Install QT from the installer

- Download the version which matches the one in `$APP_DIR/pyqtdeploy-app/sysroot.json`

For instance `qt-opensource-linux-x64-5.12.2.run` can be downloaded at: https://download.qt.io/archive/qt/5.12/5.12.2/

- After downloading the installer:
```
cd ~/Downloads
chmod +x qt*.run
./qt<Enter-Tab>
```

A Qt window will appear on which you can sign up.

Verify your email and register as an individual (no need for location).

- Restart the Qt installer with: `./qt<Enter-Tab>`
- Log in, state that you are an individual and not a company
- Setup will start
- Select folder location `~/Qt5.12.2`
- Installation will start

_Note: if custom installation has to be selected, make sure you only setup Qt5.12.2 and the default packages._

_Note2: make sure that you can access `$HOME/Qt5.12.2/5.12.2` and that the folder `android_arm64_v8a` is located inside of it._

3) Install Android Studio

- Download Android Studio (latest version) from: https://developer.android.com/studio

_Note: at the time of writing, it is version 2022.2.1.18, which can be downloaded at: https://redirector.gvt1.com/edgedl/android/studio/ide-zips/2022.2.1.18/android-studio-2022.2.1.18-linux.tar.gz_

- Extract the contents of the `.tar.gz` using `tar -xvf <tar_file>` and move the contents of `android-studio` to `$HOME` directory using `mv android-studio ~/`
- Start the installation with:
```
cd ~/android-studio/bin
./studio.sh
```

The installer will start. Do not import settings. Select custom installation.

_Note: deselect Virtual Device if you don't need it for testing_

_Note2: keep a note of the Sdk installation path, which should be `$HOME/Android/Sdk`_

Start the download (unless you want to install extra features)

- Confirm the installation of the SDK in `$HOME/Android/Sdk`

_Note: you can also confirm that `$HOME/Android/Sdk/platforms` contains `android-28` folder only.
If not, follow the instructions at the next step to set things up correctly._

4) Install correct Android SDK and Tools

- Restart Android Studio with the command provided (skip if no SDK found)
- On the menu screen, click on "more options" and then "SDK manager"
- At this point, it is recommended to use MAX Android v9.0 (Pie) = android-28 because it is the latest version of the working NDK (v19)

_Note: It might be possible to install a later NDK and thus a later android version_

- Confirm that the right SDK has been installed and get the API level (in the example, 28)

Therefore, make sure that in the "SDK Platforms tab", the following is installed: (Android 9.0) Android SDK Platform 28, (Android 9.0) Sources for Android 28.
Remove any additional unneeded package from the list.

And make sure that in the "SDK Tools tab", the following is installed (you might need to untick Hide Obsolete Packages and tick Show Package Details): (Android SDK Build-Tools 34-rc3) 33.0.2, Android Emulator, Android SDK Platform-tools, Android SDK Tools (Obsolete)

- Close Android Studio

5) Install Android NDK matching with Qt version

- Download NDK 19c from: https://dl.google.com/android/repository/android-ndk-r19c-linux-x86_64.zip

_Note: this NDK is known to be working with Qt5.12.2, but there might be others_

- Extract the contents into `~/Android` using `sudo apt-get install unzip` and `unzip <zip_file>` such that `~/Android/android-ndk-r19c` is the desired folder

_Note: make sure that `~/Android/android-ndk-r19c/platforms` contains the folder `android-28`_

6) Install Java for Android Studio

Install a stable java jdk available for your Ubuntu distribution and tested with Gradle:

```
sudo apt install openjdk-8-jdk openjdk-8-jre
```

Confirm the version with `java -version` which should be v1.8.0_362.

7) Setup the environment variables

- A file called `path_setup.sh` has been added to `$APP_DIR/pyqtdeploy-app/resources` to set up the environment variables.

Load the environment variables with:
```
source $APP_DIR/pyqtdeploy-app/resources/path_setup.sh
```

### Build the apk with pyqtdeploy

- Start the building process of the .apk with:
```
cd $APP_DIR/pyqtdeploy-app
python3 build-app.py --target android-64 --source-dir $RESOURCES_DIR --installed-qt-dir $QT_DIR --verbose
``` 
- Let the app build (it may take a while).

_Note: the app is built when you see "BUILD SUCCESSFUL"_

### Debugging

No issues reported.

### Test the .apk

- The generated `example-pyqt5-app-debug.apk` can be found in `$APP_DIR/pyqtdeploy-app/build-android-64/example-pyqt5-app/build/outputs/apk/debug`
- Copy, install and run the .apk onto your phone (>=Android v9.0)

### Customise the app for Android (optional)

Refer to "Adding Android specific things" in https://github.com/kviktor/pyqtdeploy-android-build.

### PyQt5 modules and features (optional)

1) Add images

Use QPixmap and pyrcc to save images and render them.

2) Manage your python app in android

Review python modules to create a structured project folder with writable paths.

## Build from a complex pyqt-demo app (optional)

_This section explains how to create an .apk from the more complex pyqt-demo app._

### Pre-requisites

Get rid of `$APP_DIR/pyqtdeploy-app` folder:

```
sudo rm -r $APP_DIR/pyqtdeploy-app
```

### Get the build files for pyqtdeploy

1) Get the pyqt-demo folder

- Download the pyqt-demo folder from: https://pypi.org/project/pyqtdeploy/2.5.1/#files

_Note: make sure that you get the matching pyqtdeploy version you installed with pip_

_Note2: stick to v2.x as v3.x had some major changes which will generate loads of issues_

2) Extract the contents of the `.tar.gz`

- Copy the contents into `$APP_DIR`

*Note: you should now have a folder called `$APP_DIR/pyqtdeploy-2.5.1`*

### Setup your app folder to build an apk with pyqtdeploy

1) Create new folder called `pyqtdeploy-app`

```
cd $APP_DIR
mkdir pyqtdeploy-app
```

- Copy the contents of `$APP_DIR/pyqtdeploy-2.5.1/demo` into `$APP_DIR/pyqtdeploy-app`
- Delete `$APP_DIR/pyqtdeploy-app/pyqt-demo.py`
- Rename `$APP_DIR/pyqtdeploy-app/build-demo.py` into `$APP_DIR/pyqtdeploy-app/build-app.py`
- Replace the line `shutil.copy('pyqt-demo.py', os.path.join('data', 'pyqt-demo.py.dat'))` in `build-app.py` with:
```
shutil.copy('../example-pyqt5-app.py', os.path.join('data', 'example-pyqt5-app.py.dat'))
```
- Rename all occurrences of `pyqt-demo` into `example-pyqt5-app` in `$APP_DIR/pyqtdeploy-app/build-app.py`
- Rename `$APP_DIR/pyqtdeploy-app/pyqt-demo.pdy` into `$APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy`
- Update the `$APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy` with the necessary packages:
```
cd $APP_DIR/pyqtdeploy-app
pyqtdeploy example-pyqt5-app.pdy
```
- Update the location of the main script file in `$APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy`: use the file explorer to find `example-pyqt5-app.py`
- Rename `pyqt-demo.py.dat` inside of `$APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy` with vim into: `example-pyqt5-app.py.dat`
- Check your python version (in your virtual environment) and make the version in `$APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy` match: select the right one
- In the PyQt Modules tab of `$APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy`, select your relevant Qt modules. For instance: QtCore, QtWidgets.

_Note that the .pdy might force include some default Qt modules like: QtGui, sip_

- In the Standard Library tab of `$APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy`, remove all the extra modules and keep only the default ones. If needed for your app, add more.

- Update `$APP_DIR/pyqtdeploy-app/sysroot.json` to reflect the packages selected in `$APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy` and the desired versions
- Remove the following packages (for the example) from `$APP_DIR/pyqtdeploy-app/sysroot.json`: openssl, zlib, pyqt3d, pyqtchart, pyqtdatavisualization, pyqtpurchasing, qscintilla
- Keep the following packages (for the example) in `$APP_DIR/pyqtdeploy-app/sysroot.json`: qt5 version 5.12.2, python update to version 3.6.9 (the version in your virtual environment), sip version 4.19.15, pyqt5 version 5.12.1 (even though v.5.15.6 installed in virtual environment)
- in pyqt5 section of `$APP_DIR/pyqtdeploy-app/sysroot.json`, update the list of android modules to match `$APP_DIR/pyqtdeploy-app/example-pyqt5-app.pdy`:
```
        "android#modules":              [
                "QtCore", "QtGui", "QtWidgets"
        ],
```

### Setup, build and test the app

Please follow the steps in section "Example App Demo" to setup, build and test your own pyqt5 app.

## Setup in VirtualBox (optional)

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

## Credits

_This section details the main contributors and sources for the creation of the repo._

Repository created by Achille Martin.

Donations accepted as hard work has been put into this repository, and if you feel you can make progress with your projects by converting your pyqt5 apps into Android apps.

Inspiration from:
- https://github.com/kviktor/pyqtdeploy-android-build
- https://medium.com/@Lola_Dam/packaging-pyqt-application-using-pyqtdeploy-for-both-linux-and-android-32ac7824708b

