#!/usr/bin/env python3

# Code inspired from https://www.pythonguis.com/tutorials/pyqt-qgraphics-vector-graphics/

# Tip to handle various views and scenes at:
# https://kb.froglogic.com/squish/qt/howto/getting-qgraphicsview-object-screen-geometry/

# More on GraphicsView at:
# https://doc.qt.io/qtforpython-5/overviews/graphicsview.html

# QGraphicsItem resources at:
# https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QGraphicsItem.html

# Create custom QGraphics Signals at:
# https://stackoverflow.com/questions/47079461/pyside-pyqt5-how-to-emit-signals-from-a-qgraphicsitem

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem, QStatusBar, QLabel, QGridLayout, QPushButton, QWidget
from PyQt5.QtGui import QBrush, QPen, QPainter
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    
    def __init__(self):
        
        super().__init__()
        
        # Set main window title
        self.setWindowTitle("Basic geometry shape visualiser")
        
        # Create components of the main window
        self.create_graphics_visualiser()
        self.create_statusbar()

        # Display the main window
        self.show()

    def create_graphics_visualiser(self):
            
        # 1) Define a central widget with a specific layout
        # Tip: QLayout cannot be set on the MainWindow directly
        self.graphics_window = QWidget()
        self.setCentralWidget(self.graphics_window)
        self.graphics_window_layout = QGridLayout()
        self.graphics_window.setLayout(self.graphics_window_layout)
        
        # 2) Define control buttons
        self.home_button = QPushButton("Go to Home Page")

        # 3) Define a scene for the Graphics

        # Define a scene rect of custom dimensions (width x height), with its origin at 0,0.
        # If we don't set this on creation, we can set it later with .setSceneRect
        self.scene_width = 400
        self.scene_height = 200
        self.scene = QGraphicsScene(0, 0, self.scene_width, self.scene_height)

        # Add a grid background
        self.scene.setBackgroundBrush(QBrush(Qt.lightGray, Qt.CrossPattern))

        # Draw a point item at (0, 0)
        self.origin = QGraphicsEllipseItem(-2, -2, 4, 4)
        self.origin.setBrush(QBrush(Qt.red))

        # Draw x axis
        self.x_axis_pos = QGraphicsRectItem(0, -0.5, self.scene_width, 1)
        self.x_axis_pos.setBrush(QBrush(Qt.black))

        # Draw y axis
        self.y_axis_pos = QGraphicsRectItem(-0.5, 0, 1, self.scene_height)
        self.y_axis_pos.setBrush(QBrush(Qt.black))

        # Draw a rectangle item with top-left corner at (0, 0) and set its dimensions (w, h)
        self.rect = QGraphicsRectItem(0, 0, 200, 50)

        # Set the origin of the rectangle in the scene.
        self.rect.setPos(50, 20)

        # Define the painting options for the rectangle
        self.brush = QBrush(Qt.magenta)
        self.rect.setBrush(self.brush)
        self.pen = QPen(Qt.cyan)
        self.pen.setWidth(5)
        self.rect.setPen(self.pen)

        # Draw an ellipse item at (0, 0) and set its dimensions (a, b)
        self.ellipse = QGraphicsEllipseItem(0, 0, 100, 100)

        # Set the origin of the ellipse in the scene
        self.ellipse.setPos(75, 50)

        # Define the painting options for the ellipse
        self.brush = QBrush(Qt.blue)
        self.ellipse.setBrush(self.brush)
        self.pen = QPen(Qt.green)
        self.pen.setWidth(5)
        self.ellipse.setPen(self.pen)

        # Add the items to the scene
        # Note: items are stacked in the order they are added
        # That means: items added later will always appear on top of items added first
        self.scene.addItem(self.rect)
        self.scene.addItem(self.ellipse)
        self.scene.addItem(self.origin)
        self.scene.addItem(self.x_axis_pos)
        self.scene.addItem(self.y_axis_pos)

        # Arrange stacking order with the z coordinate to create levels
        # For instance:
        # * Z<0 for the background
        # * Z=0 for the axes
        # * Z=1 for the first level
        # * Z=2 for the second level (above the first)
        self.x_axis_pos.setZValue(-1)
        self.y_axis_pos.setZValue(-1)
        self.origin.setZValue(0)
        self.ellipse.setZValue(1)
        self.rect.setZValue(2)

        # Set properties of items
        self.ellipse.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.rect.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

        # Perform operations on the items
        self.rect.setRotation(45)

        # Track position of an object
        # print(self.ellipse.ItemPositionChange)
        # Standard events related to the scene can be found at:
        # https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QGraphicsScene.html
        self.scene.changed.connect(lambda: self.on_scene_change(self.scene, self.rect))
        self.scene.changed.connect(lambda: self.on_scene_change(self.scene, self.ellipse))
        
        # 4) Define a view for the Graphics

        # Define a view associated to the scene
        self.view = QGraphicsView(self.scene)

        # Render the view with antialiasing
        self.view.setRenderHint(QPainter.Antialiasing)
        
        # 5) Update the widgets in the selected layout
        self.graphics_window_layout.addWidget(self.home_button, 0, 0)
        self.graphics_window_layout.addWidget(self.view, 1, 0)
 
    def create_statusbar(self):
        
        # Instantiate a status bar
        self.status_bar = QStatusBar()
        
        # Define the status bar as part of the main window
        self.setStatusBar(self.status_bar)

        # object_centre_track_label.setVisible(True)
        
        # Set text for the status bar
        self.object_centre_tracker_label = QLabel()
        self.status_bar_text_init = ""
        self.object_centre_tracker_label.setText(self.status_bar_text_init)
        self.status_bar.addWidget(self.object_centre_tracker_label)
        
    def on_scene_change(self, scene, item):

        # print("Scene changes")
        if item in scene.selectedItems():

            # Get properties of an object (for exploration)
            # print("----- Attributes of ellipse -----")
            # print(self.ellipse.__dir__())
            # print("----- Attributes of ellipse rect -----")
            # print(self.ellipse.rect().__dir__())
            # print("----- Ellipse shape -----")
            # print(self.ellipse.shape())
            
            item_centre_x = item.pos().x() + item.rect().width()/2
            item_centre_y = item.pos().y() + item.rect().height()/2 

            self.status_bar_text = "Selected item centre coordinates: ({}, {})".format(round(item_centre_x, 2), round(item_centre_y, 2))
            self.object_centre_tracker_label.setText(self.status_bar_text)


if __name__ == '__main__':

    # Define the app object/instance
    app = QApplication(sys.argv)
    
    # Create a Qt widget, which will be our window.
    main_window = MainWindow()
    
    # Start the event loop and handle the exit code
    sys.exit(app.exec())

