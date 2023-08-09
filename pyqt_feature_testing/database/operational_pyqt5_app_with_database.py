#!/usr/bin/env python3

# Operational pyqt5 app with database

# Inspiration from:
# * https://www.tutorialspoint.com/pyqt5/pyqt5_database_handling.htm
# * https://realpython.com/python-pyqt-database/

## Imports

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QDialog, QTableView, QVBoxLayout, QWidget
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

        logger.debug("MainWindow::__init__ - Exited method")

    def on_button_clicked(self):
        
        # Diplay debug message and alert message
        logger.debug("MainWindow::on_button_clicked - Entered method")
        logger.info("MainWindow::on_button_clicked - Button has been clicked")
        alert = QMessageBox()
        alert_msg = """
        You clicked the button!
        
        This will open a database viewer and modifier.
        
        The app folder is: """
        alert_msg += str(app_folder)
        alert.setText(alert_msg)
        logger.debug("MainWindow::on_button_clicked - Alert message started")
        alert.exec()
        logger.debug("MainWindow::on_button_clicked - Alert message terminated")
        
        # Database viewer and modifier
        db_manager = DbManager('QSQLITE', 'sportsdatabase.db', app_folder)
        table_model = QSqlTableModel()
        db_manager.initialise_model(table_model)

        view_primary = db_manager.create_view("Table Model (View Primary)", table_model)
        view_primary.clicked.connect(db_manager.find_row)

        dlg = QDialog(self)
        layout = QVBoxLayout()
        layout.addWidget(view_primary)

        button_add_row = QPushButton("Add a row")
        button_add_row.clicked.connect(lambda: db_manager.add_row(table_model))
        layout.addWidget(button_add_row)

        button_del_row = QPushButton("Delete a row")
        button_del_row.clicked.connect(lambda: table_model.removeRow(view_primary.currentIndex().row()))
        layout.addWidget(button_del_row)

        dlg.setLayout(layout)
        dlg.setWindowTitle("Database Demo")
        logger.debug("MainWindow::on_button_clicked - Database dialog started")
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
        self.db_name = db_name # Include the extension in the name (e.g. `test.db`)
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
        query.exec_("create table sportsmen(id int primary key, ""firstname varchar(20), lastname varchar(20))")

        query.exec_("insert into sportsmen values(101, 'Roger', 'Federer')")
        query.exec_("insert into sportsmen values(102, 'Christiano', 'Ronaldo')")
        query.exec_("insert into sportsmen values(103, 'Ussain', 'Bolt')")
        query.exec_("insert into sportsmen values(104, 'Sachin', 'Tendulkar')")
        query.exec_("insert into sportsmen values(105, 'Saina', 'Nehwal')")
        logger.debug("DbManager::create_db - Created table of sportsmen with initial values")
        logger.debug("DbManager::create_db - Exited method")
        return True

    def initialise_model(self, model):
        logger.debug("DbManager::initialise_model - Entered method")
        model.setTable('sportsmen')
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

    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication(sys.argv)

    # Create a Qt widget, which will be our window.
    main_window = MainWindow()
    main_window.show()  # IMPORTANT - Windows are hidden by default.
    
    # Start the event loop.
    logger.info("main - App started")
    app.exec()
    logger.info("main - App terminated")
    
    # Your application won't reach here until you exit and the event
    # loop has stopped.
    logger.debug("main - Exited function")

if __name__ == "__main__":    
    main()
