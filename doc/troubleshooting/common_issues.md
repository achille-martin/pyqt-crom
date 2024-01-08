# Common issues

<a id="toc"></a>
## Table of Contents

* [1. Troubleshooting](#troubleshooting)
    * [1.1. Module not found](#module-not-found)
    * [1.2. File not found](#file-not-found)
    * [1.3. Setup repo with a Virtual Machine](#virtual-machine-setup)

<a id="troubleshooting"></a>
## 1. Troubleshooting

:mag: This section walks you through tips and fixes for the main challenges you might encounter.

<a id="module-not-found"></a>
### 1.1. Module not found

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
### 1.2. File not found

If the [building process](#apk-build) or any other process fails because some files cannot be found, ensure that you have correctly setup your `.bashrc` to load the environment.

Go through the [Getting started](#getting-started) tutorial and confirm the state of your `.bashrc`.

<a id="virtual-machine-setup"></a>
### 1.3. Setup repo with a Virtual Machine

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

