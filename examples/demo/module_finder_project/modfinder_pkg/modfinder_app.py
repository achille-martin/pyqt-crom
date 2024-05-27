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

# Module Finder PyQt5 app
# Inspired by Martin Fitzpatrick from https://www.pythonguis.com/tutorials/creating-your-first-pyqt-window/
#
# This app helps you identify
# the python module dependencies
# related to specific non-standard python libraries


## Imports

import sys
sys_modules = dict(sorted(sys.modules.items()))
sys_modules_base = list(sys_modules.keys())
sys_modules_base.sort()

import_error_msg = ""
sys_modules_base_with_pkg = None
sys_modules_pkg = None
try:
    # Import your non-standard python pkg
    import numpy
    sys_modules = dict(sorted(sys.modules.items()))
    sys_modules_base_with_pkg = list(sys_modules.keys())
    sys_modules_base_with_pkg.sort()
    sys_modules_pkg = list(
        set(
            sys_modules_base_with_pkg
        ).difference(
            set(sys_modules_base)
        )
    )
    sys_modules_pkg.sort()
except Exception as e:
    import_error_msg = f"Exception caught: {e}"

import os
import logging as log_tool  # The logging library for debugging
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt5.QtCore import QStandardPaths

built_in_modules = list(sys.stdlib_module_names)
built_in_modules.sort()

## Main variables and objects

# Retrieve app data folder path reference
std_app_data_folder_path_list = QStandardPaths.writableLocation(
    QStandardPaths.AppDataLocation
)

# Define custom app data folder path
std_app_data_folder_path = ""
if isinstance(std_app_data_folder_path_list, list):
    std_app_data_folder_path = std_app_data_folder_path_list[0]
else:
    std_app_data_folder_path = str(std_app_data_folder_path_list)
app_data_folder_path = os.path.join(
    std_app_data_folder_path, 
    'pyqt5_app_data', 
)

# Generate custom app data folder at convenient writable location
os.makedirs(app_data_folder_path, exist_ok = True)

# Set logger config and instantiate object
logger_logging_level = "DEBUG"
logger_output_file_name = "modfinder_app.log"
logger_output_prefix_format = "[%(asctime)s] [%(levelname)s] - %(message)s"
logger = log_tool.getLogger(__name__)
logger.setLevel(logger_logging_level)
logger_output_file_path = os.path.join(app_data_folder_path, str(logger_output_file_name))
file_handler = log_tool.FileHandler(logger_output_file_path)
formatter = log_tool.Formatter(logger_output_prefix_format)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Set additional log output location
# for non-root debugging
# when flag is_non_root_debug_active is set to True
is_non_root_debug_active = True
# WARNING: this feature might require 
# to allow storage access permission before launching the app
if is_non_root_debug_active:
    # Retrieve documents folder path reference
    # to save logs at a location accessible by non-root users
    std_documents_folder_path_list = QStandardPaths.writableLocation(
        QStandardPaths.DocumentsLocation
    )
    # Define custom alternative app data folder path
    std_documents_folder_path = ""
    if isinstance(std_documents_folder_path_list, list):
        std_documents_folder_path = std_documents_folder_path_list[0]
    else:
        std_documents_folder_path = str(std_documents_folder_path_list)
    alternative_app_data_folder_path = os.path.join(
        std_documents_folder_path, 
        'pyqt5_app_data', 
    )
    # Generate alternative app data folder at convenient writable location
    os.makedirs(alternative_app_data_folder_path, exist_ok = True)
    # Add log file output alternative to logger
    logger_output_file_path_alternative = os.path.join(
        alternative_app_data_folder_path, 
        str(logger_output_file_name)
    )
    file_handler_alternative = log_tool.FileHandler(
        logger_output_file_path_alternative
    )
    formatter_alternative = log_tool.Formatter(logger_output_prefix_format)
    file_handler_alternative.setFormatter(formatter_alternative)
    logger.addHandler(file_handler_alternative)

## Investigating the imports
logger.debug("---- SYS MODULES BASE ----")
logger.debug(sys_modules_base)
logger.debug("---- SYS MODULES BASE WITH PKG ----")
logger.debug(sys_modules_base_with_pkg)
logger.debug("---- SYS MODULES NUMPY ----")
logger.debug(sys_modules_pkg)
logger.debug("---- PYTHON BUILT-IN MODULES ----")
logger.debug(built_in_modules)
logger.debug("---- IMPORT ERRORS ----")
logger.debug(import_error_msg)


## Class definition

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Module Finder PyQt5 app")

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
