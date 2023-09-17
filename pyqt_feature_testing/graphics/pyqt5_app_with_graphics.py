#!/usr/bin/env python3

# Code inspired from https://www.pythonguis.com/tutorials/pyqt-qgraphics-vector-graphics/

import sys
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QApplication, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtGui import QBrush, QPen, QPainter
from PyQt5.QtCore import Qt

if __name__ == '__main__':

    # 1) Define the app object
    app = QApplication(sys.argv)
    
    # 2) Define the scene

    # Define a scene rect of 400x200, with it's origin at 0,0.
    # If we don't set this on creation, we can set it later with .setSceneRect
    scene_width = 400
    scene_height = 200
    scene = QGraphicsScene(0, 0, scene_width, scene_height)

    # Add a grid background
    scene.setBackgroundBrush(QBrush(Qt.lightGray, Qt.CrossPattern))
    
    # Draw a point item at (0, 0)
    origin = QGraphicsEllipseItem(-2, -2, 4, 4)
    origin.setBrush(QBrush(Qt.red))

    # Draw x axis
    x_axis_pos = QGraphicsRectItem(0, -0.5, scene_width, 1)
    x_axis_pos.setBrush(QBrush(Qt.black))
    
    # Draw y axis
    y_axis_pos = QGraphicsRectItem(-0.5, 0, 1, scene_height)
    y_axis_pos.setBrush(QBrush(Qt.black))

    # Draw a rectangle item with top-left corner at (0, 0) and set its dimensions (w=200, h=50)
    rect = QGraphicsRectItem(0, 0, 200, 50)

    # Set the origin (50, 20) of the rectangle in the scene.
    rect.setPos(50, 20)
     
    # Define the painting options for the rectangle
    brush = QBrush(Qt.magenta)
    rect.setBrush(brush)
    pen = QPen(Qt.cyan)
    pen.setWidth(5)
    rect.setPen(pen)
    
    # Draw an ellipse item at (0, 0) and set its dimensions (a=100, b=100)
    ellipse = QGraphicsEllipseItem(0, 0, 100, 100)

    # Set the origin (75, 50) of the ellipse in the scene
    ellipse.setPos(75, 50)

    # Define the painting options for the ellipse
    brush = QBrush(Qt.blue)
    ellipse.setBrush(brush)
    pen = QPen(Qt.green)
    pen.setWidth(5)
    ellipse.setPen(pen)

    # Add the items to the scene
    # Note: items are stacked in the order they are added
    # That means: items added later will always appear on top of items added first
    scene.addItem(rect)
    scene.addItem(ellipse)
    scene.addItem(origin)
    scene.addItem(x_axis_pos)
    scene.addItem(y_axis_pos)

    # Arrange stacking order with the z coordinate to create levels
    # For instance:
    # * Z<0 for the background
    # * Z=0 for the axes
    # * Z=1 for the first level
    # * Z=2 for the second level (above the first)
    x_axis_pos.setZValue(-1)
    y_axis_pos.setZValue(-1)
    origin.setZValue(0)
    ellipse.setZValue(1)
    rect.setZValue(2)

    # Set properties of items
    ellipse.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
    rect.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

    # Perform operations on the items
    rect.setRotation(45)

    # Track an object
    print("----- Attributes of ellipse -----")
    print(ellipse.__dir__())
    print("----- Ellipse centre position -----")
    ellipse_centre_x = 0 
    ellipse_centre_y = 0

    # 3) Define the view

    # Define a view associated to the scene
    view = QGraphicsView(scene)

    # Render the view with antialiasing
    view.setRenderHint(QPainter.Antialiasing)

    # Display the view in the scene
    view.show()
    
    # 4) Handle app loops
    sys.exit(app.exec_())
