#!/usr/bin/env python3

# Example simple pyqt5 app
# Inspired by: https://www.pythonguis.com/tutorials/creating-your-first-pyqt-window/

## Imports

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox

# Only needed for access to command line arguments
# import sys

## Class definition

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Example simple pyqt5 app")

        button = QPushButton("Press Here for the magic")

        button.setCheckable(True)
        button.clicked.connect(self.on_button_clicked)

        # Set properties of the  widget in the Window.
        self.setMaximumSize(QSize(400, 300))
        self.setCentralWidget(button)


    def on_button_clicked(self):
        print("Button has been clicked!")
        alert = QMessageBox()
        alert.setText('You clicked the button!')
        alert.exec()


## Application definition

def main():

    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication([])

    # Create a Qt widget, which will be our window.
    main_window = MainWindow()
    main_window.showMaximized()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec()

    # Your application won't reach here until you exit and the event
    # loop has stopped.

if __name__ == "__main__":
    # This needs to only define main
    # due to how pyqtdeploy is implemented to build packages
    main()
