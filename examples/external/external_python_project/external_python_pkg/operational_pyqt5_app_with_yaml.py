#!/usr/bin/env python3

# MIT License

# Copyright (c) 2024 Achille MARTIN

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

# PyQt5 app with PyYAML

## Imports

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt5.QtCore import QStandardPaths
from yaml import safe_load
from os import makedirs
from os.path import isfile, realpath, dirname, join, exists
import logging as log_tool  # The logging library for debugging
import sys

## Main variables and objects

# Retrieve app data folder path reference
std_app_data_folder_path_list = QStandardPaths.writableLocation(
    QStandardPaths.AppDataLocation
)
if std_app_data_folder_path_list is None:
    sys.exit("[ERROR] Cannot find writable App Data folder path")

# Define app data folder path
std_app_data_folder_path = ""
if isinstance(std_app_data_folder_path_list, list):
    std_app_data_folder_path = std_app_data_folder_path_list[0]
else:
    std_app_data_folder_path = str(std_app_data_folder_path_list)
app_data_folder_path = join(std_app_data_folder_path, 'pyqt5_app_data', 'pyqt5_app_with_yaml')

# Generate app data folder at convenient writable location
makedirs(app_data_folder_path, exist_ok = True)

# Set logger config and instantiate object
logger_logging_level = "DEBUG"
logger_output_file_name = "pyqt5-app-with-yaml.log"
logger_output_prefix_format = "[%(asctime)s] [%(levelname)s] - %(message)s"
logger = log_tool.getLogger(__name__)
logger.setLevel(logger_logging_level)
logger_output_file_path = join(app_data_folder_path, str(logger_output_file_name))
file_handler = log_tool.FileHandler(logger_output_file_path)
formatter = log_tool.Formatter(logger_output_prefix_format)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Define app config content
app_config_content = \
f"""
app_name: "PyQt5 app with YAML"
target_performance:
  min_app_load_speed_s: 3
  max_nb_crash_allowed: 0
"""
app_config_file_name = "app_config.yaml"


## Class definition

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialise class attributes
        self.setWindowTitle("PyQt5 app with YAML")
        
        # Initialise button
        button = QPushButton("Press Here for the magic")
        button.setCheckable(True)
        button.clicked.connect(self.on_button_clicked)
        
        # Generate app config source as yaml file
        self.app_config_file_path = join(app_data_folder_path, app_config_file_name)
        with open(self.app_config_file_path, "w") as file:
            file.write(app_config_content)
        logger.debug(
            f"MainWindow::__init__ - Generated app config in: {self.app_config_file_path}"
        )
        
        # Import app config from yaml file
        app_config = self.import_yaml_config(self.app_config_file_path)
        self.app_name = app_config.get('app_name', '')
        target_performance_details = app_config.get('target_performance', dict())
        self.min_app_load_speed_s = target_performance_details.get('min_app_load_speed_s', '')
        self.max_nb_crash_allowed = target_performance_details.get('max_nb_crash_allowed', '')

        # Set properties of the  widget in the Window
        self.setCentralWidget(button)

    def on_button_clicked(self):
        
        # Display alert message
        alert = QMessageBox()
        alert.setText(
            f"""
            You clicked the button!
            
            Loaded config file for the app: {self.app_name}
            
            The target performance is:
            * Min app loading speed = {self.min_app_load_speed_s} s
            * Max number of crashes allowed = {self.max_nb_crash_allowed}

            Config file path `{app_config_file_name}` 
            is located in: {self.app_config_file_path} 
            """
        )
        alert.exec()

    def import_yaml_config(self, config_file_path):
        empty_dict = dict()
        config = empty_dict
        # Check whether config file exists
        if not isfile(config_file_path):
            logger.debug(
                    f"""
                    MainWindow::import_yaml_config -
                    Cannot import yaml config from `{config_file_path}`
                    Because file does not exist
                    Returning empty dictionary
                    """
            )
            return empty_dict

        # Import yaml config from file
        with open(config_file_path, 'r') as file:
            config = safe_load(file)
        logger.debug(
                f"""
                MainWindow::import_yaml_config -
                Imported yaml config from `{config_file_path}`:
                {config}
                """
        )
        return config


## Application definition

def main():
    logger.info("========================\n")
    logger.info("========================")
    logger.debug(f"main - Log output file can be found at: {logger_output_file_path}")
    # Only one QApplication instance is needed per application.
    # Pass in sys.argv to allow command line arguments for the app: `QApplication(sys.argv)`
    # If command line arguments are not needed, use: `QApplication([])`
    app = QApplication([])

    # Create a QMainWindow object which represents the Main Window.
    main_window = MainWindow()
    main_window.showMaximized()  # This line will show windows that are normally hidden. Plus, it will maximise the main window.

    # Start the application event loop.
    logger.info("main - App started")
    sys.exit(app.exec())
    logger.info("main - App terminated")

    # The application will only reach here when exiting or event loop has stopped.

if __name__ == "__main__":
    # This section needs to only define main
    # due to how pyqtdeploy is implemented to build packages
    main()
