#!/usr/bin/env python3

# MIT License

# Copyright (c) 2023-2024 Achille MARTIN

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Demo PyQt5 app
# Inspired by Martin Fitzpatrick from https://www.pythonguis.com/tutorials/creating-your-first-pyqt-window/

## Imports

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox

# Only needed for access to command line arguments
# import sys

## Class definition

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Demo PyQt5 app")

        button = QPushButton("Press Here for the magic")

        button.setCheckable(True)
        button.clicked.connect(self.on_button_clicked)

        # Set properties of the  widget in the Window.
        self.setCentralWidget(button)


    def on_button_clicked(self):
        print("Button has been clicked!")
        alert = QMessageBox()
        alert.setText('You clicked the button!')
        alert.exec()


## Application definition

def main():
    # Only one QApplication instance is needed per application.
    # Pass in sys.argv to allow command line arguments for the app: `QApplication(sys.argv)`
    # If command line arguments are not needed, use: `QApplication([])`
    app = QApplication([])

    # Create a QMainWindow object which represents the Main Window.
    main_window = MainWindow()
    main_window.showMaximized()  # This line will show windows that are normally hidden. Plus, it will maximise the main window.

    # Start the application event loop.
    app.exec()

    # The application will only reach here when exiting or event loop has stopped.

if __name__ == "__main__":
    # This section needs to only define main
    # due to how pyqtdeploy is implemented to build packages
    main()
