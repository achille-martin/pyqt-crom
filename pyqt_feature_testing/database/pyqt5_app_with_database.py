#!/usr/bin/env python3

# Code inspired from https://www.tutorialspoint.com/pyqt5/pyqt5_database_handling.htm

import sys
import os.path
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
    query.exec_("create table sportsmen(id int primary key, ""firstname varchar(20), lastname varchar(20))")

    query.exec_("insert into sportsmen values(101, 'Roger', 'Federer')")
    query.exec_("insert into sportsmen values(102, 'Christiano', 'Ronaldo')")
    query.exec_("insert into sportsmen values(103, 'Ussain', 'Bolt')")
    query.exec_("insert into sportsmen values(104, 'Sachin', 'Tendulkar')")
    query.exec_("insert into sportsmen values(105, 'Saina', 'Nehwal')")
    return True

def initializeModel(model):
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

def addrow():
    # print ("Model row number: " + str(model.rowCount()))
    ret = model.insertRows(model.rowCount(), 1)
    # print ("Model insert state: " + str(ret))

def findrow(i):
    delrow_ = i.row()

if __name__ == '__main__':
    
    # Parameter setting
    db_type_ = 'QSQLITE'
    db_name_ = 'sportsdatabase.db'
    db_folder_ = './'
    delrow_ = -1
    
    # Database creation
    if not os.path.exists(db_folder_ + db_name_):
        createDB(db_type_, db_name_)
    
    # Database target
    app = QApplication(sys.argv)
    db = QSqlDatabase.addDatabase(db_type_)
    db.setDatabaseName(db_name_)
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
