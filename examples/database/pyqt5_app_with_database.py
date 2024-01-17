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

# Code inspired from Tutorials Point at https://www.tutorialspoint.com/pyqt5/pyqt5_database_handling.htm

import sys
import os.path # To manage file paths for cross-platform apps
from PyQt5.QtSql import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

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
    query.exec_("create table tennismen(id int primary key, ""firstname varchar(20), lastname varchar(20))")

    query.exec_("insert into tennismen values(101, 'Andre', 'Agassi')")
    query.exec_("insert into tennismen values(102, 'Novak', 'Djokovic')")
    query.exec_("insert into tennismen values(103, 'Daniil', 'Medvedev')")
    query.exec_("insert into tennismen values(104, 'Andy', 'Murray')")
    query.exec_("insert into tennismen values(105, 'Rafael', 'Nadal')")
    return True

def initializeModel(model):
    model.setTable('tennismen')
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

def addrow():
    # print ("Model row number: " + str(model.rowCount()))
    ret = model.insertRows(model.rowCount(), 1)
    # print ("Model insert state: " + str(ret))

def findrow(i):
    delrow_ = i.row()

if __name__ == '__main__':
    
    # Parameter setting
    db_type_ = 'QSQLITE'
    db_name_ = 'sportsdatabase.db' # Include the extension in the name (e.g. `test.db`)
    app_folder_ = os.path.dirname(os.path.realpath(__file__)) # App folder is the one containing this script
    db_folder_ = app_folder_
    delrow_ = -1
    
    # Database creation
    if not os.path.exists(os.path.join(db_folder_, db_name_)):
        createDB(db_type_, os.path.join(db_folder_, db_name_))
    
    # Database target
    app = QApplication(sys.argv)
    db = QSqlDatabase.addDatabase(db_type_)
    db.setDatabaseName(os.path.join(db_folder_, db_name_))
    model = QSqlTableModel()
    initializeModel(model)

    view1 = createView("Table Model (View 1)", model)
    view1.clicked.connect(findrow)

    dlg = QDialog()
    layout = QVBoxLayout()
    layout.addWidget(view1)

    button = QPushButton("Add a row")
    button.clicked.connect(addrow)
    layout.addWidget(button)

    btn1 = QPushButton("del a row")
    btn1.clicked.connect(lambda: model.removeRow(view1.currentIndex().row()))
    layout.addWidget(btn1)

    dlg.setLayout(layout)
    dlg.setWindowTitle("Database Demo")
    dlg.show()
    sys.exit(app.exec_()) 
