# Origin story

<a id="toc"></a>
## Table of Contents

* [1. How it all began...](#original-story)
    * [1.1. A fresh start](#fresh-start)
    * [1.2. Get the build files for pyqtdeploy](#original-build-files)
    * [1.3. Setup an app folder to build an .apk with pyqtdeploy](#original-setup)
    * [1.4. Setup, build and test the app](#original-build)

<a id="original-story"></a>
## 1. How it all began...

:mag: This section shows you how this repo came to life by leveraging the functionalities of [pyqtdeploy](https://pypi.org/project/pyqtdeploy/).

<a id="fresh-start"></a>
### 1.1. A fresh start

Get rid of `$SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app` folder:

```
sudo rm -r $SIMPLE_PYQT5_ANDROID_APP_DIR/pyqtdeploy_app
```

<a id="original-build-files"></a>
### 1.2. Get the build files for pyqtdeploy

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
### 1.3. Setup an app folder to build an .apk with pyqtdeploy

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
### 1.4. Setup, build and test the app

Please follow the steps detailed in [Getting Started](#getting-started) to setup, build and test your own PyQt5 app.

If you would like to understand how `pyqtdeploy` works and how to set it up, please refer to the [official tutorial](https://docs.huihoo.com/pyqt/pyqtdeploy/tutorial.html).

[:arrow_heading_up: Back to TOP](#toc) 
