# PyQt5 Features

:mag: This section introduces the main PyQt5 features you will need to create your custom app.

<a id="toc"></a>
## Table of Contents

* [1. Databases](#pyqt5-databases)
    * [1.1. Engine selection](#engine-selection)
    * [1.2. Setup for database management](#database-management-setup)
    * [1.3. Example PyQt5 app](#database-pyqt5-demo-app)
    * [1.4. Example operational PyQt5 app](#operational-database-pyqt5-demo-app)
* [2. Graphics](#pyqt5-graphics)
    * [2.1. 2D Graphics](#pyqt5-2d-graphics)
    * [2.2. Example PyQt5 app](#graphics-pyqt5-demo-app)
    * [2.3. Example operational PyQt5 app](#operational-graphics-pyqt5-demo-app)

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
#### 1.3. Example PyQt5 app

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
#### 1.4. Example operational PyQt5 app

You can also run a more operational PyQt5 app boasting a database with:

```
cd $PYQT_CROM_DIR/pyqt_feature_testing/database
python3 operational_pyqt5_app_with_database.py
```

This demo app is built on the one highlighted in the [Getting started](../../README.md#getting-started) section:
- A window appears on the screen in a window with 2 buttons: MAGIC or EXIT
- Once MAGIC is clicked, a pop-up appears on screen stating that the button has been clicked and that a database will open
- Once the pop-up has been acknowledged, a database (called `sportsdatabase.db`) is created in the `home` folder as shown in the alert window, if not already existing
- In the dialog window displaying the content of the database, rows can be added, removed or edited

:point_up: _You can view the content of `sportsdatabase.db` at any time by following the instructions in [Example PyQt5 app with database](#database-pyqt5-demo-app) after ensuring that your [Database manager](#database-management-setup) is correctly setup._

!! ADD DEMO VIDEO OF DATABASE MANAGEMENT ANDROID APP !!

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
#### 2.2. Example PyQt5 app

To visualise a basic example of 2D Graphics in a PyQt app, run the following:


```
cd $PYQT_CROM_DIR/pyqt_feature_testing/graphics
python3 pyqt5_app_with_graphics.py
```

A graphics window will appear, in which you can perform the following:

* Move shapes around and locate their centre thanks to the status bar prompt
* Get back to the home screen thanks to the button at the top of the window

<a id="operational-graphics-pyqt5-demo-app"></a>
#### 2.3. Example operational PyQt5 app

You can also run a more operational PyQt5 app boasting a graphics playground with:

```
cd $PYQT_CROM_DIR/pyqt_feature_testing/graphics
python3 operational_pyqt5_app_with_graphics.py
```

This demo app is built on the one highlighted in the [Getting started](../../README.md#getting-started) section:
- A window appears on the screen in a window with 2 buttons: MAGIC or EXIT
- Once MAGIC is clicked, a pop-up appears on screen stating that the button has been clicked and that a graphics playground will open
- Once the pop-up has been acknowledged, a graphics playground opens up with 2 shapes that can be dragged around
- When selecting a shape, its coordinates are displayed at the bottom of the screen, in the status bar
- To exit the graphics playground, hit the HOME button

!! ADD DEMO VIDEO OF GRAPHICS PLAYGROUND ANDROID APP !!

[:arrow_heading_up: Back to TOP](#toc)

[:house: Back to HOME](../../README.md)

