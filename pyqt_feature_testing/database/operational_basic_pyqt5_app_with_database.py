#!/usr/bin/env python3

# Operational pyqt5 app with database

# Inspiration from:
# * https://www.tutorialspoint.com/pyqt5/pyqt5_database_handling.htm
# * https://realpython.com/python-pyqt-database/

## Imports

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QDialog, QTableView, QVBoxLayout
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

import sys
import os.path # To manage file paths for cross-platform apps

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
        
        # Diplay debug message and alert message
        alert = QMessageBox()
        alert.setText('You clicked the button!\n\nThis will open a database viewer and modifier...')
        alert.exec()
        
        # Database viewer and modifier
        app_folder = os.path.expanduser('~')
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
        dlg.exec()

# Database Manager class
class DbManager():
   
    # Ensure one connection to a database per application
    db_connected = None
    
    def __init__(self, db_type, db_name, db_folder):

        self.db_type = db_type
        self.db_name = db_name # Include the extension in the name (e.g. `test.db`)
        self.db_folder = db_folder
        self.delrow = -1
        
        if DbManager.db_connected is None:
            try:
                DbManager.db_connected = QSqlDatabase.addDatabase(self.db_type)
                DbManager.db_connected.setDatabaseName(os.path.join(self.db_folder, self.db_name))
            except Exception as error:
                pass
        else:
            pass

        # Initial database creation
        if not os.path.exists(os.path.join(self.db_folder, self.db_name)):
            self.create_db()

    def __del__(self):
        self.db_connected.close()

    def create_db(self):
        if not self.db_connected.open():
          msg = QMessageBox()
          msg.setIcon(QMessageBox.Critical)
          msg.setText("Error in Database Creation")
          retval = msg.exec_()
          return False

        query = QSqlQuery()
        query.exec_("create table sportsmen(id int primary key, ""firstname varchar(20), lastname varchar(20))")

        query.exec_("insert into sportsmen values(101, 'Roger', 'Federer')")
        query.exec_("insert into sportsmen values(102, 'Christiano', 'Ronaldo')")
        query.exec_("insert into sportsmen values(103, 'Ussain', 'Bolt')")
        query.exec_("insert into sportsmen values(104, 'Sachin', 'Tendulkar')")
        query.exec_("insert into sportsmen values(105, 'Saina', 'Nehwal')")
        return True

    def initialise_model(self, model):
        model.setTable('sportsmen')
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select()
        model.setHeaderData(0, Qt.Horizontal, "ID")
        model.setHeaderData(1, Qt.Horizontal, "First name")
        model.setHeaderData(2, Qt.Horizontal, "Last name")

    def create_view(self, title, model):
        view = QTableView()
        view.setModel(model)
        view.setWindowTitle(title)
        return view

    def add_row(self, model):
        # print ("Model row number: " + str(model.rowCount()))
        ret = model.insertRows(model.rowCount(), 1)
        # print ("Model insert state: " + str(ret))

    def find_row(self, i):
        self.delrow = i.row()

## Application definition

def main():

    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication(sys.argv)

    # Create a Qt widget, which will be our window.
    main_window = MainWindow()
    main_window.show()  # IMPORTANT - Windows are hidden by default.
    
    # Start the event loop.
    app.exec()
    
    # Your application won't reach here until you exit and the event
    # loop has stopped.

if __name__ == "__main__":    
    # This needs to only define main    
    # due to how pyqtdeploy is implemented to build packages    
    main()
