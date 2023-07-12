#!/usr/bin/env python3

# Operational pyqt5 app

## Imports

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QDialog, QTableView, QVBoxLayout
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

import sys
import os.path

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
        alert.setText('You clicked the button!\n\nThis will open a database viewer and modifier...')
        alert.exec()
        
        # Database creation
        if not os.path.exists(db_folder_ + db_name_):
            createDB(db_type_, db_name_)
        
        # Database viewer and modifier
        db = QSqlDatabase.addDatabase(db_type_)
        db.setDatabaseName(db_name_)
        model = QSqlTableModel()
        initialiseModel(model)

        view1 = createView("Table Model (View 1)", model)
        view1.clicked.connect(findrow)

        dlg = QDialog(self)
        layout = QVBoxLayout()
        layout.addWidget(view1)

        button = QPushButton("Add a row")
        button.clicked.connect(lambda: addrow(model))
        layout.addWidget(button)

        btn1 = QPushButton("del a row")
        btn1.clicked.connect(lambda: model.removeRow(view1.currentIndex().row()))
        layout.addWidget(btn1)

        dlg.setLayout(layout)
        dlg.setWindowTitle("Database Demo")
        dlg.exec()

## Extra function definition

def createDB(db_type, db_name):
    db = QSqlDatabase.addDatabase(db_type)
    db.setDatabaseName(db_name)

    if not db.open():
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

def initialiseModel(model):
    model.setTable('sportsmen')
    model.setEditStrategy(QSqlTableModel.OnFieldChange)
    model.select()
    model.setHeaderData(0, Qt.Horizontal, "ID")
    model.setHeaderData(1, Qt.Horizontal, "First name")
    model.setHeaderData(2, Qt.Horizontal, "Last name")

def createView(title, model):
    view = QTableView()
    view.setModel(model)
    view.setWindowTitle(title)
    return view

def addrow(model):
    # print ("Model row number: " + str(model.rowCount()))
    ret = model.insertRows(model.rowCount(), 1)
    # print ("Model insert state: " + str(ret))

def findrow(i):
    delrow_ = i.row()

## Database definition

# Primary help link:  https://www.tutorialspoint.com/pyqt5/pyqt5_database_handling.htm
# Secondary help link: https://realpython.com/python-pyqt-database/

# Parameter setting
db_type_ = 'QSQLITE'
db_name_ = 'sportsdatabase.db'
db_folder_ = './'
delrow_ = -1

## Application definition

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
main_window = MainWindow()
main_window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.
