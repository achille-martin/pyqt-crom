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

# PyQt5 app with Py YAML

## Imports

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
# from yaml import safe_load
from os.path import isfile, realpath

# Only needed for access to command line arguments
# import sys

## Class definition

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialise class attributes
        self.setWindowTitle("Demo PyQt5 app")
        
        # Initialise button
        button = QPushButton("Press Here for the magic")
        button.setCheckable(True)
        button.clicked.connect(self.on_button_clicked)

        # Import yaml config
        config_file_path = 'example_config.yaml'
        app_config = self.import_yaml_config(config_file_path)
        self.app_name = app_config.get('app_name', '')
        target_performance_config = app_config.get('target_performance', dict())
        self.min_app_load_speed_s = target_performance_config.get('min_app_load_speed_s', '')
        self.max_nb_crash_allowed = target_performance_config.get('max_nb_crash_allowed', '')

        # Set properties of the  widget in the Window.
        self.setCentralWidget(button)

    def on_button_clicked(self):
        
        print("Button has been clicked!")
         
        # Display alert message
        alert = QMessageBox()
        alert.setText(
            f"""
            You clicked the button!
            
            Loded config file for app:
            {self.app_name}
            
            The target performance is:
            * Minimum app loading speed = {self.min_app_load_speed_s} s
            * Maximum number of crashes allowed = {self.max_nb_crash_allowed}
            """
        )
        alert.exec()

    def import_yaml_config(self, config_file_path):
        empty_dict = dict()
        config = empty_dict
        # Check whether config file exists
        if not isfile(config_file_path):
            print(
                    f"""
                    Cannot import yaml config from {config_file_path}
                    Because file does not exist
                    Returning empty dict
                    """
            )
            return empty_dict

        # Import yaml config from file
        # with open(config_file_path, 'r') as file:
        #     config = safe_load(file)
        print(
                f"""
                Imported yaml config from {realpath(config_file_path)}:
                {config}
                """
        )
        return config


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
