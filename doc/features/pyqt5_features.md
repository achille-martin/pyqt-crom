# PyQt5 Features

:mag: This section introduces the main PyQt5 features needed to create a custom standard app.

<a id="toc"></a>
## Table of Contents

* [1. Databases](#pyqt5-databases)
    * [1.1. Engine selection](#engine-selection)
    * [1.2. Setup for database management](#database-management-setup)
    * [1.3. Example PyQt5 Database app](#database-pyqt5-demo-app)
    * [1.4. Example operational PyQt5 Database app](#operational-database-pyqt5-demo-app)
* [2. Graphics](#pyqt5-graphics)
    * [2.1. 2D Graphics](#pyqt5-2d-graphics)
    * [2.2. Example PyQt5 Graphics app](#graphics-pyqt5-demo-app)
    * [2.3. Example operational PyQt5 Graphics app](#operational-graphics-pyqt5-demo-app)
* [3. Network](#pyqt5-network)
    * [3.1. Bluetooth](#pyqt5-bluetooth)
    * [3.2. Example PyQt5 Bluetooth app](#bluetooth-pyqt5-demo-app)
    * [3.3. Example operational PyQt5 Bluetooth app](#operational-bluetooth-pyqt5-demo-app)

<a id="pyqt5-databases"></a>
### 1. Databases

<a id="engine-selection"></a>
#### 1.1. Engine selection

The preferred database engine for Android is `SQLite`. The latest SQLite library available is `sqlite3` as introduced on [the SQLite website](https://www.sqlite.org/version3.html).

PyQt5 lets you work with many other database engines as shown on [tutorialspoint website](https://www.tutorialspoint.com/pyqt5/pyqt5_database_handling.htm), but `sqlite3` is a good start for simple python apps because:
- The application file is portable across multiple platforms
- Reading/writing performance is great as the application only loads the data it needs
- Content is updated continuously and atomically for maximum reliability
- Database content can be viewed with many third-party tools

<a id="database-management-setup"></a>
#### 1.2. Setup for database management

Before attempting to run any `SQLite`-related actions, make sure that the library is available on your machine:

```
sudo apt-get install sqlite3
sudo apt-get install sqlitebrowser
```

<a id="database-pyqt5-demo-app"></a>
#### 1.3. Example PyQt5 Database app

To confirm that `SQLite` is functional on your machine, run the following:

```
cd $PYQT_CROM_DIR/examples/database
python3 pyqt5_app_with_database.py
```

A dialog window will pop up in which you can perform the following:
- View the pre-populated database (called `sportsdatabase.db`)
- Add a row to the database
- Remove a row from the database

You can view the content of the generated and edited database at any time outside of the application with:

```
cd $PYQT_CROM_DIR/examples/database
sqlitebrowser sportsdatabase.db
```

<a id="operational-database-pyqt5-demo-app"></a>
#### 1.4. Example operational PyQt5 Database app

You can also run a more operational PyQt5 app boasting a database with:

```
cd $PYQT_CROM_DIR/examples/database/database_management_project/database_management_pkg
python3 operational_pyqt5_app_with_database.py
```

This demo app is built on the one highlighted in the [Getting started](../../README.md#getting-started) section:
- A window appears on the screen in a window with 2 buttons: MAGIC or EXIT
- Once MAGIC is clicked, a pop-up appears on screen stating that the button has been clicked and that a database will open
- Once the pop-up has been acknowledged, a database (called `sportsdatabase.db`) is created in the `home` folder as shown in the alert window, if not already existing
- In the dialog window displaying the content of the database, rows can be added, removed or edited

:bulb: _You can view the content of `sportsdatabase.db` at any time by following the instructions in [Example PyQt5 app with database](#database-pyqt5-demo-app) after ensuring that your [Database manager](#database-management-setup) is correctly setup._

<a id="pyqt5-database-management-app-android-video"></a>

<video src="https://github.com/achille-martin/pyqt-crom/assets/66834162/5368d162-e8fe-42c0-bd25-cfed5c647ddb">
   <p>PyQt5 database management app Android platform video</p>
</video>

<a id="pyqt5-graphics"></a>
### 2. Graphics

<a id="pyqt5-2d-graphics"></a>
#### 2.1. 2D Graphics

There are 2 main approaches to create 2D Graphics in Qt apps:
* QGraphics way
* QtQuick way

QGraphics relies on a database of useful shapes and widgets (QWidgets) to make the app efficient and native (the look is tied to the platform). As described on the [pythonguis website](https://www.pythonguis.com/tutorials/pyqt-qgraphics-vector-graphics/), QGraphics harnesses the model-view paradigm through QGraphicsScene (model), QGraphicsView (view) and QGraphicsItems (visual elements).

QtQuick on the other hand, relies on the Qt Modeling language (QML) to define user interfaces. As described on the [pythonguis website](https://www.pythonguis.com/tutorials/qml-qtquick-python-application/), QML is focused on custom UI design and is useful for consistent app design across multiple platforms. The look of the app will be more modern, but the development might take longer.

As we are showcasing a prototyping tool for mobile apps, we have decided to explore QGraphics options rather than follow QtQuick practices. Note that both approaches are viable and handled by the pyqtdeploy tool.

<a id="graphics-pyqt5-demo-app"></a>
#### 2.2. Example PyQt5 Graphics app

To visualise a basic example of 2D Graphics in a PyQt app, run the following:


```
cd $PYQT_CROM_DIR/examples/graphics
python3 pyqt5_app_with_graphics.py
```

A graphics window will appear, in which you can perform the following:

* Move shapes around and locate their centre thanks to the status bar prompt
* Get back to the home screen thanks to the button at the top of the window

<a id="operational-graphics-pyqt5-demo-app"></a>
#### 2.3. Example operational PyQt5 Graphics app

You can also run a more operational PyQt5 app boasting a graphics playground with:

```
cd $PYQT_CROM_DIR/examples/graphics/graphics_playground_project/graphics_playground_pkg
python3 operational_pyqt5_app_with_graphics.py
```

This demo app is built on the one highlighted in the [Getting started](../../README.md#getting-started) section:
- A window appears on the screen in a window with 2 buttons: MAGIC or EXIT
- Once MAGIC is clicked, a pop-up appears on screen stating that the button has been clicked and that a graphics playground will open
- Once the pop-up has been acknowledged, a graphics playground opens up with 2 shapes that can be dragged around
- When selecting a shape, its coordinates are displayed at the bottom of the screen, in the status bar
- To exit the graphics playground, hit the HOME button

<a id="pyqt5-graphics-playground-app-android-video"></a>

<video src="https://github.com/achille-martin/pyqt-crom/assets/66834162/d1089522-c7e6-4ea4-953d-eb20550bbd96">
   <p>PyQt5 graphics playground app Android platform video</p>
</video>

<a id="pyqt5-network"></a>
#### 3. Network

Network is used to interface multiple devices. The network helps interconnect devices to extend the capabilities of the application.

<a id="pyqt5-bluetooth"></a>
#### 3.1. Bluetooth

The first simple type of network communication is Bluetooth (which is more practical than wired connection).

There are 2 main types of Bluetooth technologies:

* Classic (used for audio streaming)
* Low Energy (LE) (used for any other application)

A bigger comparison between Bluetooth Classic and Bluetooth LE is made on [symmetryelectronics website](https://www.symmetryelectronics.com/blog/the-difference-between-classic-bluetooth-and-bluetooth-low-energy/).

Since the aim is not to stream audio, we will solely focus on Bluetooth LE.

<a id="bluetooth-pyqt5-demo-app"></a>
#### 3.2. Example PyQt5 Bluetooth app

QtBluetooth classes are very powerful and enable the cross-platform use of Bluetooth communications.

A set of classes is introduced on the [official qt website](https://doc.qt.io/qtforpython-6/PySide6/QtBluetooth/index.html#module-PySide6.QtBluetooth).

QtBluetooth classes are used in this basic example of Bluetooth communications from a PyQt app. To run the example Bluetooth app, use:


```
cd $PYQT_CROM_DIR/examples/network
python3 pyqt5_app_with_bluetooth.py
```

The example Bluetooth app provides the following experience:
- A window appears on the screen with 2 buttons: Search for Bluetooth devices and EXIT
- If you click on EXIT, the app will close itself
- If you click on Search for Bluetooth devices, the app will ask you whether your device is Bluetooth capable. If it is not, the app is actually unusable and will crash. If you do have Bluetooth on your device, you will be asked to turn it ON.
- Once your Bluetooth is ON, click again on Search for Bluetooth devices so that the app can search for nearby devices for 5 seconds
- The app displays the list of found nearby devices on the main window

If you encounter issues with Bluetooth, please refer to the [Bluetooth troubleshooting](../troubleshooting/commong_issues.md#virtual-machine-bluetooth).

<a id="operational-bluetooth-pyqt5-demo-app"></a>
#### 3.3. Example operational PyQt5 Bluetooth app

To visualise an operational example of Bluetooth communications in a PyQt app, run the following:

```
cd $PYQT_CROM_DIR/examples/network/bluetooth_scanner_project/bluetooth_scanner_pkg
python3 operational_pyqt5_app_with_bluetooth.py
```

The operational example Bluetooth app has a similar behaviour to the [example Bluetooth app](#bluetooth-pyqt5-demo-app).

If you encounter issues with Bluetooth, please refer to the [Bluetooth troubleshooting](../troubleshooting/commong_issues.md#virtual-machine-bluetooth).

[:arrow_heading_up: Back to TOP](#toc)

[:house: Back to HOME](../../README.md)

