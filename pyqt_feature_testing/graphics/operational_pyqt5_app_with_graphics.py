#!/usr/bin/env python3

# Code inspired from https://www.pythonguis.com/tutorials/pyqt-qgraphics-vector-graphics/

# Stacked layout to manage pages inspired from https://realpython.com/python-pyqt-layout/

## Imports

from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem, QStatusBar, QLabel, QGridLayout, QPushButton, QWidget, QMessageBox, QStackedLayout
from PyQt5.QtGui import QBrush, QPen, QPainter
from PyQt5.QtCore import Qt

import sys
import os.path # To manage file paths for cross-platform apps
import logging as log_tool # The logging library for debugging

## Main variables and objects

# Define path reference: app folder is the reference for the device
app_folder = os.path.expanduser('~')
if not os.path.exists(app_folder):
    # Ensure that a path can be defined to generate the necessary files on device
    app_folder = os.getcwd()

# Set logger config and instantiate object
logger_logging_level = "DEBUG"
logger_output_file_name = "pyqt5-app.log"
logger_output_prefix_format = "[%(asctime)s] [%(levelname)s] - %(message)s"

logger = log_tool.getLogger(__name__)
logger.setLevel(logger_logging_level)
logger_output_file_path = os.path.join(app_folder, str(logger_output_file_name))
file_handler = log_tool.FileHandler(logger_output_file_path)
formatter = log_tool.Formatter(logger_output_prefix_format)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

## Class definition

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        logger.debug("MainWindow::__init__ - Entered method")
        
        # Set main window title
        self.setWindowTitle("Example simple pyqt5 geometric shape visualiser")
        
        # Create a stacked layout to switch between widget display (app "screens")
        self.stacked_layout = QStackedLayout()
        self.stacked_layout_dict = {} # Dict mapping screen index with screen name

        # Create components of the main window
        self.create_home_page()
        self.create_graphics_visualiser()
        self.create_statusbar()

        # Display the main window
        self.showMaximized() # Maximise the main window

        logger.debug("MainWindow::__init__ - Exited method")
 
    def create_home_page(self):

        logger.debug("MainWindow::create_home_page - Entered method")
        
        # Define a central widget with a specific layout
        home_screen = QWidget()
        home_screen_layout = QGridLayout()
        home_screen.setLayout(home_screen_layout)
        self.setCentralWidget(home_screen)
        self.stacked_layout.addWidget(home_screen)
        self.stacked_layout_dict["home"] = 0

        logger.debug("MainWindow::create_home_page - Updated stacked layout: " + str(self.stacked_layout_dict))

        # Instantiate buttons for the home screen
        button_magic = QPushButton("Press HERE for the MAGIC")
        button_exit = QPushButton("Press HERE to EXIT")
        
        # Attach callbacks to buttons
        button_magic.setCheckable(True)
        button_magic.clicked.connect(self.on_button_magic_clicked)

        button_exit.setCheckable(True)
        button_exit.clicked.connect(self.close)

        # Update the widgets in the selected layout
        home_screen_layout.addWidget(button_magic, 1, 1, 1, 1)
        home_screen_layout.addWidget(button_exit, 3, 1, 1, 1)
        home_screen_layout.setRowStretch(0, 1)
        home_screen_layout.setRowStretch(2, 1)
        home_screen_layout.setRowStretch(4, 1)
        home_screen_layout.setColumnStretch(0, 1) 
        home_screen_layout.setColumnStretch(2, 1) 
        
        logger.debug("MainWindow::create_home_page - Exited method")

    def on_button_magic_clicked(self):
        
        logger.debug("MainWindow::on_button_magic_clicked - Entered method")
        logger.info("MainWindow::on_button_magic_clicked - Button has been clicked")

        # Create alert pop-up message
        alert = QMessageBox()
        alert.setWindowTitle("Information")
        alert_msg = """
        You clicked the button!

        This will open a graphics visualiser.
        """
        alert.setText(alert_msg)

        # Add standard buttons to the alert pop-up and set OK as default
        alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        alert.setDefaultButton(QMessageBox.Ok)

        # Start the alert pop-up
        logger.debug("MainWindow::on_button_magic_clicked - Alert message started")
        # Note: do not maximise alert windows as it might lead to button display issues
        alert_value = alert.exec()

        # Return to home screen if user cancels the alert pop-up
        if alert_value == QMessageBox.Cancel:
            alert.close()
            logger.debug("MainWindow::on_button_magic_clicked - Alert message terminated")
        # Proceed to next screen if user accepts alert pop-up
        else:
            alert.close()
            logger.debug("MainWindow::on_button_magic_clicked - Alert message terminated")
            self.status_bar.setVisible(True) # Make status bar visible
            self.stacked_layout.setCurrentIndex(self.stacked_layout_dict["graphics"])

    def create_graphics_visualiser(self):
            
        # Define a central widget with a specific layout
        # Tip: QLayout cannot be set on the MainWindow directly
        graphics_screen = QWidget()
        self.setCentralWidget(graphics_screen)
        graphics_screen_layout = QGridLayout()
        graphics_screen.setLayout(graphics_screen_layout)
        self.stacked_layout.addWidget(graphics_screen)
        self.stacked_layout_dict["graphics"] = 1

        # Define control buttons
        home_button = QPushButton("Go to Home Page")
        home_button.clicked.connect(self.on_home_button_clicked)

        # Define a scene for the Graphics

        # Define a scene rect of custom dimensions (width x height), with its origin at 0,0.
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

        # Draw a rectangle item with top-left corner at (0, 0) and set its dimensions (w, h)
        rect = QGraphicsRectItem(0, 0, 200, 50)

        # Set the origin of the rectangle in the scene.
        rect.setPos(50, 20)

        # Define the painting options for the rectangle
        brush_rect = QBrush(Qt.magenta)
        rect.setBrush(brush_rect)
        pen_rect = QPen(Qt.cyan)
        pen_rect.setWidth(5)
        rect.setPen(pen_rect)

        # Draw an ellipse item at (0, 0) and set its dimensions (a, b)
        ellipse = QGraphicsEllipseItem(0, 0, 100, 100)

        # Set the origin of the ellipse in the scene
        ellipse.setPos(75, 50)

        # Define the painting options for the ellipse
        brush_ellipse = QBrush(Qt.blue)
        ellipse.setBrush(brush_ellipse)
        pen_ellipse = QPen(Qt.green)
        pen_ellipse.setWidth(5)
        ellipse.setPen(pen_ellipse)

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
        # self.rect.setRotation(45)

        # Track position of an object
        # print(self.ellipse.ItemPositionChange)
        # Standard events related to the scene can be found at:
        # https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QGraphicsScene.html
        scene.changed.connect(lambda: self.on_scene_change(scene, rect))
        scene.changed.connect(lambda: self.on_scene_change(scene, ellipse))
        
        # Define a view for the Graphics

        # Define a view associated to the scene
        view = QGraphicsView(scene)

        # Render the view with antialiasing
        view.setRenderHint(QPainter.Antialiasing)
        
        # Update the widgets in the selected layout
        graphics_screen_layout.addWidget(home_button, 0, 1, 1, 1)
        graphics_screen_layout.addWidget(view, 1, 0, 1, 3)
        graphics_screen_layout.setRowStretch(0, 0)
        graphics_screen_layout.setColumnStretch(0, 1)
        graphics_screen_layout.setColumnStretch(2, 1)

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

    def on_home_button_clicked(self):
        
        # Instantiate the alert message for the home button
        alert = QMessageBox()
        alert.setText('You will be redirected to the home page...')

        # Add standard buttons to the alert pop-up and set OK as default
        alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        alert.setDefaultButton(QMessageBox.Ok)

        # Start the alert pop-up
        alert_value = alert.exec()

        # Return to graphics screen if user cancels the alert pop-up
        if alert_value == QMessageBox.Cancel:
            alert.close()
        # Proceed to next screen if user accepts alert pop-up
        else:
            alert.close()
            self.status_bar.setVisible(False) # Make status bar invisible
            self.stacked_layout.setCurrentIndex(self.stacked_layout_dict["home"])

    def on_scene_change(self, scene, item):

        # print("Scene changes")
        if item in scene.selectedItems():

            item_centre_x = item.pos().x() + item.rect().width()/2
            item_centre_y = item.pos().y() + item.rect().height()/2 

            self.status_bar_text = "Selected item centre coordinates: ({}, {})".format(round(item_centre_x, 2), round(item_centre_y, 2))
            self.object_centre_tracker_label.setText(self.status_bar_text)

## Application definition

def main():
    logger.info("========================\n")
    logger.info("========================")
    logger.debug("main - Entered function and logger instantiated")
    logger.debug("main - Log output file can be found at: " + str(logger_output_file_path))

    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication(sys.argv)

    # Create a Qt widget, which will be our window.
    main_window = MainWindow()
    
    # Start the event loop and handle the exit code
    logger.info("main - App started")
    sys.exit(app.exec())
    logger.info("main - App terminated")
    
    # Your application won't reach here until you exit and the event
    # loop has stopped.
    logger.debug("main - Exited function")

if __name__ == "__main__":    
    main()

