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

# Operational pyqt5 app with database

# Inspiration from Tutorials Point at https://www.tutorialspoint.com/pyqt5/pyqt5_database_handling.htm
# And from Pozo Ramos at https://realpython.com/python-pyqt-database/

## Imports

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QDialog, QTableView, QVBoxLayout, QWidget, QSizePolicy
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

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

        self.setWindowTitle("Example simple pyqt5 app")
        
        # Create a widget to serve as layout for the main window
        widget_main_window = QWidget(self)
        self.setCentralWidget(widget_main_window)
        layout_main_window = QVBoxLayout()
        widget_main_window.setLayout(layout_main_window)
        
        # Instantiate buttons for the main window
        button_magic = QPushButton("Press HERE for the MAGIC")
        button_exit = QPushButton("Press HERE to EXIT")
        
        # Add buttons to the main window layout
        layout_main_window.addWidget(button_magic)
        layout_main_window.addWidget(button_exit)

        # Attach callbacks to buttons
        button_magic.setCheckable(True)
        button_magic.clicked.connect(self.on_button_clicked)

        button_exit.setCheckable(True)
        button_exit.clicked.connect(self.close)
        
        # Ensure buttons resize to the whole window
        button_magic.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_exit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set the main window to show as maximised
        self.showMaximized()

        logger.debug("MainWindow::__init__ - Exited method")

    def on_button_clicked(self):
        
        logger.debug("MainWindow::on_button_clicked - Entered method")
        logger.info("MainWindow::on_button_clicked - Button has been clicked")

        # Create alert window message
        alert = QMessageBox()
        alert.setWindowTitle("Information")
        alert_msg = """
        You clicked the button!
        
        This will open a database viewer and modifier.
        
        The app folder is: """
        alert_msg += str(app_folder)
        alert.setText(alert_msg)

        # Add standard buttons to the alert window and set OK as default
        alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        alert.setDefaultButton(QMessageBox.Ok)
        
        # Start the window
        logger.debug("MainWindow::on_button_clicked - Alert message started")
        # Note: do not maximise alert windows as it might lead to button display issues
        alert_value = alert.exec()

        # Return to main window if user cancels alert window
        if alert_value == QMessageBox.Cancel:
            alert.close()
            logger.debug("MainWindow::on_button_clicked - Alert message terminated")
        # Proceed to next window if user accepts alert window
        else:
            logger.debug("MainWindow::on_button_clicked - Alert message terminated")
        
            # Instantiate the database manager
            db_manager = DbManager('QSQLITE', 'sportsdatabase.db', app_folder)
            table_model = QSqlTableModel()
            db_manager.initialise_model(table_model)

            view_primary = db_manager.create_view("Table Model (View Primary)", table_model)
            view_primary.clicked.connect(db_manager.find_row)
            
            # Create a window to display the database viewer and modifier
            dlg = QDialog(self)
            layout_database_window = QVBoxLayout()
            layout_database_window.addWidget(view_primary)
            
            # Add buttons to the window to interact with the database viewer and modifier
            button_add_row = QPushButton("Add a row")
            button_add_row.clicked.connect(lambda: db_manager.add_row(table_model))
            layout_database_window.addWidget(button_add_row)

            button_del_row = QPushButton("Delete a row")
            button_del_row.clicked.connect(lambda: table_model.removeRow(view_primary.currentIndex().row()))
            layout_database_window.addWidget(button_del_row)

            button_done = QPushButton("Done")
            button_done.clicked.connect(dlg.close)
            layout_database_window.addWidget(button_done)
            
            # Set layout and start the window
            dlg.setLayout(layout_database_window)
            dlg.setWindowTitle("Database Demo")
            logger.debug("MainWindow::on_button_clicked - Database dialog started")
            dlg.showMaximized()
            dlg.exec()
            logger.debug("MainWindow::on_button_clicked - Database dialog terminated")
            logger.debug("MainWindow::on_button_clicked - Exited method")

# Database Manager class
class DbManager():
   
    # Ensure one connection to a database per application
    db_connected = None
    
    def __init__(self, db_type, db_name, db_folder):
        logger.debug("DbManager::__init__ - Entered method")

        self.db_type = db_type
        # Include the extension in the name (e.g. `test.db`)
        self.db_name = db_name 
        self.db_folder = db_folder
        self.delrow = -1
        
        if DbManager.db_connected is None:
            try:
                DbManager.db_connected = QSqlDatabase.addDatabase(self.db_type)
                DbManager.db_connected.setDatabaseName(os.path.join(self.db_folder, self.db_name))
            except Exception as error:
                logger.exception("DbManager::__init__ - Error: Connection not established - " + str(error))
            else:
                logger.info("DbManager::__init__ - Connection established for " 
                        + str(self.db_name) 
                        + " of type " 
                        + str(self.db_type) 
                        + " at location " 
                        + str(os.path.join(self.db_folder, self.db_name))
                        )

        # Initial database creation
        if not os.path.exists(os.path.join(self.db_folder, self.db_name)):
            self.create_db()

        logger.info("DbManager::__init__ - Database Manager for " 
                + str(os.path.join(self.db_folder, self.db_name)) 
                + " instantiated"
                )

        logger.debug("DbManager::__init__ - Exited method")

    def __del__(self):
        logger.debug("DbManager::__del__ - Entered method")
        self.db_connected.close()
        logger.info("DbManager::__del__ - Database Manager for " 
                + str(os.path.join(self.db_folder, self.db_name)) 
                + " deleted"
                )
        logger.debug("DbManager::__del__ - Exited method")

    def create_db(self):
        logger.debug("DbManager::create_db - Entered method")
        if not self.db_connected.open():
          msg = QMessageBox()
          msg.setIcon(QMessageBox.Critical)
          msg.setText("Error in Database Creation")
          retval = msg.exec_()
          logger.exception("DbManager::create_db - Error in Database Creation")
          return False

        query = QSqlQuery()
        query.exec_("create table tennismen(id int primary key, ""firstname varchar(20), lastname varchar(20))")

        query.exec_("insert into tennismen values(101, 'Andre', 'Agassi')")
        query.exec_("insert into tennismen values(102, 'Novak', 'Djokovic')")
        query.exec_("insert into tennismen values(103, 'Daniil', 'Medvedev')")
        query.exec_("insert into tennismen values(104, 'Andy', 'Murray')")
        query.exec_("insert into tennismen values(105, 'Rafael', 'Nadal')")
        logger.debug("DbManager::create_db - Created table of tennismen with initial values")
        logger.debug("DbManager::create_db - Exited method")
        return True

    def initialise_model(self, model):
        logger.debug("DbManager::initialise_model - Entered method")
        model.setTable('tennismen')
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select()
        model.setHeaderData(0, Qt.Horizontal, "ID")
        model.setHeaderData(1, Qt.Horizontal, "First name")
        model.setHeaderData(2, Qt.Horizontal, "Last name")
        logger.debug("DbManager::initialise_model - Exited method")

    def create_view(self, title, model):
        logger.debug("DbManager::create_view - Entered method")
        view = QTableView()
        view.setModel(model)
        view.setWindowTitle(title)
        logger.debug("DbManager::create_view - Exited method")
        return view

    def add_row(self, model):
        logger.debug("DbManager::add_row - Entered method")
        # print ("Model row number: " + str(model.rowCount()))
        ret = model.insertRows(model.rowCount(), 1)
        # print ("Model insert state: " + str(ret))
        logger.debug("DbManager::add_row - Exited method")

    def find_row(self, i):
        logger.debug("DbManager::add_row - Entered method")
        self.delrow = i.row()
        logger.debug("DbManager::add_row - Exited method")

## Application definition

def main():
    logger.info("========================\n")
    logger.info("========================")
    logger.debug("main - Entered function and logger instantiated")
    logger.debug("main - Log output file can be found at: " + str(logger_output_file_path))

    # Only one QApplication instance is needed per application.
    # Pass in sys.argv to allow command line arguments for the app: `QApplication(sys.argv)`
    # If command line arguments are not needed, use: `QApplication([])`
    app = QApplication(sys.argv)

    # Create a QMainWindow object which represents the Main Window.
    main_window = MainWindow()
    main_window.show()  # This line will show windows that are normally hidden.
    
    # Start the application event loop and handle the exit code
    logger.info("main - App started")
    sys.exit(app.exec())
    logger.info("main - App terminated")
    
    # The application will only reach here when exiting or event loop has stopped.
    logger.debug("main - Exited function")

if __name__ == "__main__":    
    main()
