# Common issues

:mag: This section walks you through tips and fixes for the main challenges you might encounter while setting up the repo or running the scripts.

<a id="toc"></a>
## Table of Contents

* [1. Module not found](#module-not-found)
* [2. File not found](#file-not-found)
* [3. Qt plugin error](#qt-plugin-error)
* [4. Setup repo with a Virtual Machine](#virtual-machine-setup)
* [5. Setup Bluetooth in a Virtual Machine](#virtual-machine-bluetooth)
* [6. Setup an Android Emulator](#android-emulator-setup)

<a id="module-not-found"></a>
### 1. Module not found

When trying to run the PyQt5 app on your machine, the following issue might come up:

```
Traceback (most recent call last):
  File "./demo_app.py", line 8, in <module>
    from PyQt5.QtCore import QSize
ModuleNotFoundError: No module named 'PyQt5'
```

This means that the python modules have not been correctly loaded.

Please make sure that you have followed the [Getting started](../../README.md#getting-started) tutorial.

If you have followed the tutorial, then ensure that you have [activated your virtual environment](../../README.md#virtual-environment-activation).

<a id="file-not-found"></a>
### 2. File not found

If the [building process](../../README.md#app-generation) or any other process fails because some files cannot be found, ensure that you have correctly setup your `.bashrc` to load the environment: go through the [Getting started](../../README.md#getting-started) tutorial and confirm the state of your `.bashrc`.

<a id="qt-plugin-error"></a>
### 3. Qt plugin error

If you encounter Qt plugin errors (when trying to run your `PyQt5 application`), such as:

> qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.

Follow the instructions below to find the origin of the problem and solve it:

* Enable the Qt debug prints:

```
export QT_DEBUG_PLUGINS=1
```

* Run your `PyQt5 application` again to read the DEBUG prints

* Identify the issue. For instance, if it is related to the package `libxcb-xinerama`, install it with:

```
sudo apt-get install libxcb-xinerama0
```

<a id="virtual-machine-setup"></a>
### 4. Setup repo with a Virtual Machine

To setup a Linux Virtual Machine on Windows via VirtualBox, follow [It's FOSS virtualbox setup tutorial](https://itsfoss.com/install-linux-in-virtualbox/).

If you would prefer to setup a Linux Virtual Machine on MacOS via VirtualBox, follow [TecAdmin virtualbox setup tutorial](https://tecadmin.net/how-to-install-virtualbox-on-macos/).

It is also recommended to install the VirtualBox Guest Additions. Follow the [LinuxTechi guest addition setup tutorial](https://www.linuxtechi.com/install-virtualbox-guest-additions-on-ubuntu/) for more information.

:bulb: _It is also recommended to set the size of the Virtual Machine to at least 50GB so that there is enough space to download and install all dependencies._

<a id="virtual-machine-bluetooth"></a>
### 5. Setup Bluetooth in a Virtual Machine

If you are using VirtualBox (Virtual Machine) and you want to run a pyqt5 app requiring a Bluetooth connection, you can follow these steps:

* Turn ON Bluetooth on your host machine (Windows machine)
* Restart VirtualBox
* In Devices -> USB, find your Bluetooth dongle (you can find the name on Windows host by opening the `Device Manager`)
  * If you can't see the Bluetooth dongle, you might need a physical dongle to plug into your machine
* Open the Bluetooth settings on your Ubuntu client and turn the Bluetooth ON
* Run `hciconfig -a` to confirm whether the dongle is present AND running (UP)
  * If the dongle is not present, make sure that your Bluetooth dongle is ON in VirtualBox.
  * If the dongle is not running (DOWN), you can restart the Bluetooth service with `sudo systemctl restart bluetooth.service`

<a id="android-emulator-setup"></a>
### 6. Setup an Android Emulator

To setup an Android Emulator, it is recommended to use Android Studio.

_If you want to set up the Android Emulator in VirtualBox, please refer to [this issue](https://github.com/achille-martin/pyqt-crom/issues/12)._

To setup the Android Emulator in Ubuntu, make sure that you have:
* Android Studio installed (refer to [External dependencies setup](../../README.md#external-dependency-installation) if needed)
* Correctly set up Android Studio as per [Expo dev recommendations](https://docs.expo.dev/workflow/android-studio-emulator/)
* Added the following to your `$HOME/.bashrc`

```
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

* Correctly set up the virtualisation solution and solved potential issues mentioned on [Stackoverflow](https://stackoverflow.com/questions/37300811/android-studio-dev-kvm-device-permission-denied)

```
sudo apt install qemu-kvm
ls -al /dev/kvm
sudo adduser <username> kvm
sudo chown <username> /dev/kvm
```

Once the Android Emulator is set up and running, you can drag and drop your `.apk` to install it and run it.

If you wish to access more Android logs, please refer to [this issue](https://github.com/achille-martin/pyqt-crom/issues/12), which mentions tips for `adb`, the Android Debug Bridge.

[:arrow_heading_up: Back to TOP](#toc)

[:house: Back to HOME](../../README.md)
