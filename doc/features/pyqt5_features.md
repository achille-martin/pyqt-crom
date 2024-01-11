# PyQt5 Features

<a id="toc"></a>
## Table of Contents

* [1. Extra features for your Android app](#android-app-extra-features)
    * [1.1. Images](#pyqt5-images)
    * [1.2. File management](#pyqt5-file-management)
    * [1.3. Databases](#pyqt5-databases)
        * [1.3.1. Engine selection](#engine-selection)
        * [1.3.2. Setup for database management](#database-management-setup)
        * [1.3.3. Example PyQt5 app](#database-pyqt5-demo-app)
        * [1.3.4. Example operational PyQt5 app](#operational-database-pyqt5-demo-app)
    * [1.4. Graphics](#pyqt5-graphics)
        * [1.4.1. 2D Graphics](#pyqt5-2d-graphics)
        * [1.4.2. Example PyQt5 app](#graphics-pyqt5-demo-app)
        * [1.4.3. Example operational PyQt5 app](#operational-graphics-pyqt5-demo-app)

<a id="android-app-extra-features"></a>
## 1. Extra features for your Android app

:mag: This section introduces a few outstanding capabilities of PyQt5 which can be ported to your Android app.

The demo app only contains a very small set of PyQt5 features, but this section explores the full potential of PyQt5 and gives hints on how to make a fully working Android (prototype) app.

<a id="pyqt5-images"></a>
### 1.1. Images

Use `QPixmap` and `pyrcc` to save images and render them.

<a id="pyqt5-file-management"></a>
### 1.2. File management

Rely on python modules to create a structured project folder with writable paths.

<a id="pyqt5-databases"></a>
### 1.3. Databases

<a id="engine-selection"></a>
#### 1.3.1. Engine selection

The preferred database engine for Android is `SQLite`. The latest SQLite library available is `sqlite3` as introduced on [the SQLite website](https://www.sqlite.org/version3.html).

PyQt5 lets you work with many other database engines as shown on [tutorialspoint website](https://www.tutorialspoint.com/pyqt5/pyqt5_database_handling.htm), but `sqlite3` is a good start for simple python apps because:
- The application file is portable across multiple platforms
- Reading/writing performance is great as the application only loads the data it needs
- Content is updated continuously and atomically for maximum reliability
- Database content can be viewed with many third-party tools

<a id="database-management-setup"></a>
#### 1.3.2. Setup for database management

Before attempting to run any `SQLite`-related actions, make sure that the library is available on your machine:

```
sudo apt-get install sqlite3
sudo apt-get install sqlitebrowser
```

<a id="database-pyqt5-demo-app"></a>
#### 1.3.3. Example PyQt5 app

To confirm that `SQLite` is functional on your machine, run the following:

```
cd $PYQT_CROM_DIR/pyqt_feature_testing/database
python3 pyqt5_app_with_database.py
```

A dialog window will pop up in which you can perform the following:
- View the pre-populated database (called `sportsdatabase.db`)
- Add a row to the database
- Remove a row from the database

You can view the content of the generated and edited database at any time outside of the application with:

```
cd $PYQT_CROM_DIR/pyqt_feature_testing/database
sqlitebrowser sportsdatabase.db
```

<a id="operational-database-pyqt5-demo-app"></a>
#### 1.3.4. Example operational PyQt5 app

You can also run a more operational PyQt5 app boasting a database with:

```
cd $PYQT_CROM_DIR/pyqt_feature_testing/database
python3 operational_pyqt5_app_with_database.py
```

This demo app is built on the one highlighted in the [Getting started](#getting-started) section:
- A window appears on the screen in a window with 2 buttons: MAGIC or EXIT
- Once MAGIC is clicked, a pop-up appears on screen stating that the button has been clicked and that a database will open
- Once the pop-up has been acknowledged, a database (called `sportsdatabase.db`) is created in the `home` folder as shown in the alert window, if not already existing
- In the dialog window displaying the content of the database, rows can be added, removed or edited

:point_up: _You can view the content of `sportsdatabase.db` at any time by following the instructions in [Example PyQt5 app with database](#database-pyqt5-demo-app) after ensuring that your [Database manager](#database-management-setup) is correctly setup._

<a id="pyqt5-graphics"></a>
### 1.4. Graphics

<a id="pyqt5-2d-graphics"></a>
#### 1.4.1. 2D Graphics

There are 2 main approaches to create 2D Graphics in Qt apps:
* QGraphics way
* QtQuick way

QGraphics relies on a database of useful shapes and widgets (QWidgets) to make the app efficient and native (the look is tied to the platform). As described on the [pythonguis website](https://www.pythonguis.com/tutorials/pyqt-qgraphics-vector-graphics/), QGraphics harnesses the model-view paradigm through QGraphicsScene (model), QGraphicsView (view) and QGraphicsItems (visual elements).

QtQuick on the other hand, relies on the Qt Modeling language (QML) to define user interfaces. As described on the [pythonguis website](https://www.pythonguis.com/tutorials/qml-qtquick-python-application/), QML is focused on custom UI design and is useful for consistent app design across multiple platforms. The look of the app will be more modern, but the development might take longer.

As we are showcasing a prototyping tool for mobile apps, we have decided to explore QGraphics options rather than follow QtQuick practices. Note that both approaches are viable and handled by the pyqtdeploy tool.

<a id="graphics-pyqt5-demo-app"></a>
#### 1.4.2. Example PyQt5 app

To visualise a basic example of 2D Graphics in a PyQt app, run the following:


```
cd $PYQT_CROM_DIR/pyqt_feature_testing/graphics
python3 pyqt5_app_with_graphics.py
```

A graphics window will appear, in which you can perform the following:

* Move shapes around and locate their centre thanks to the status bar prompt
* Get back to the home screen thanks to the button at the top of the window

<a id="operational-graphics-pyqt5-demo-app"></a>
#### 1.4.3. Example operational PyQt5 app

You can also run a more operational PyQt5 app boasting a graphics playground with:

```
cd $PYQT_CROM_DIR/pyqt_feature_testing/graphics
python3 operational_pyqt5_app_with_graphics.py
```

This demo app is built on the one highlighted in the [Getting started](#getting-started) section:
- A window appears on the screen in a window with 2 buttons: MAGIC or EXIT
- Once MAGIC is clicked, a pop-up appears on screen stating that the button has been clicked and that a graphics playground will open
- Once the pop-up has been acknowledged, a graphics playground opens up with 2 shapes that can be dragged around
- When selecting a shape, its coordinates are displayed at the bottom of the screen, in the status bar
- To exit the graphics playground, hit the HOME button

[:arrow_heading_up: Back to TOP](#toc)

[:house: Back to HOME](../../README.md)

