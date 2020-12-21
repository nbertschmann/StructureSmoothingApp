from ParseLogs import parseLogs
from CombineTilts import combineTilts
from WriteToCSV import writeToCSV
from FormatData import formatData
from RecreateStructure import recreateStructure
from PlotArray import plotArray
from ShowQT import showQT

import PyQt5
import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication)
from PyQt5 import QtWidgets
import os
from PyQt5.QtCore import QThreadPool
from PyQt5.QtCore import QAbstractItemModel

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pandas as pd




class StructureSmooth(QWidget):
    def __init__(self):
        super().__init__()

        self.file_path = ''
        self.file_name = ''
        self.folder_path = ''
        self.folder_name = ''
        self.file_arr = []

        self.my_layout = QtWidgets.QVBoxLayout(self)

        self.pushButton1 = QPushButton("Create Plots")
        self.browse_button1 = QtWidgets.QPushButton('Browse')
        self.browse_box1 = QtWidgets.QLineEdit()

        self.plotDisplay_tab = QtWidgets.QTabWidget()

        self.browse_layout1 = QtWidgets.QHBoxLayout()
        self.browse_layout1.addWidget(self.browse_button1)
        self.browse_layout1.addWidget(self.browse_box1)

        self.tab_layout1 = QtWidgets.QVBoxLayout()
        self.tab_layout1.addLayout(self.browse_layout1)
        self.tab_layout1.addWidget(self.plotDisplay_tab)
        self.tab_layout1.addWidget(self.pushButton1)

        self.analyzeLogs_button = QtWidgets.QPushButton("Analyze Logs")
        self.browse_button2 = QtWidgets.QPushButton('Browse')
        self.browse_box2 = QtWidgets.QLineEdit()

        self.table_display = self.initTable()

        self.browse_layout2 = QtWidgets.QHBoxLayout()
        self.browse_layout2.addWidget(self.browse_button2)
        self.browse_layout2.addWidget(self.browse_box2)

        self.tab_layout2 = QtWidgets.QVBoxLayout()
        self.tab_layout2.addLayout(self.browse_layout2)
        self.tab_layout2.addWidget(self.table_display)
        self.tab_layout2.addWidget(self.analyzeLogs_button)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tab1.layout = QtWidgets.QVBoxLayout(self)
        self.tab1.layout.addLayout(self.tab_layout1)
        self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout = QtWidgets.QVBoxLayout(self)
        self.tab2.layout.addLayout(self.tab_layout2)
        self.tab2.setLayout(self.tab2.layout)

        self.select_tab = QtWidgets.QTabWidget()
        self.select_tab.addTab(self.tab1, 'Create Plots')
        self.select_tab.addTab(self.tab2, 'Analyze Logs')

        self.my_layout.addWidget(self.select_tab)
        self.setLayout(self.my_layout)
        self.initUI()

        self.connect()

    def initTable(self):

        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['DM', 'X', 'Y', 'Z', 'Pitch', 'Roll'])
        table = QtWidgets.QTableView()
        table.setModel(model)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)

        return table

    def initUI(self):

        self.setGeometry(50, 75, 1000, 900)
        self.setWindowTitle('Structure Smoothness')

        self.show()

    def connect(self):
        self.browse_button1.clicked.connect(self.browseFiles1)
        self.browse_button2.clicked.connect(self.browseFiles2)
        self.analyzeLogs_button.clicked.connect(self.analyzeLogs)

    def browseFiles1(self):

        file_path_tuple = QtWidgets.QFileDialog.getOpenFileName(self, "File Browser")

        self.file_path = file_path_tuple[0]
        file_array = self.file_path.strip().split('/')
        self.file_name = file_array[-1]

        if self.file_path:

            self.browse_box1.clear()
            self.browse_box1.insert(self.file_path)

        pass
    def browseFiles2(self):

        self.folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Folder Browser")

        folder_arr = self.folder_path.strip().split('/')
        self.folder_name = folder_arr[-1]

        if self.folder_path:
            self.browse_box2.clear()
            self.browse_box2.insert(self.folder_path)

            self.file_arr = os.listdir(self.folder_path)

    def analyzeLogs(self):

        log_array = []
        df_array = []

        for file in self.file_arr:
            if 'tblStruct' in file:
                self.structureVerfication_file = os.path.join(self.folder_path, file)
            if 'auto_output' in file:
                log_array.append(file)

        for file in log_array:
            log_path = os.path.join(self.folder_path, file)
            log_data = parseLogs(log_path, self.structureVerfication_file)
            df_array.append(log_data)

        self.log_data_raw = pd.concat(df_array)
        self.log_data_combined = combineTilts(self.log_data_raw)

        model = TableModel(self.log_data_combined)
        self.table_display.setModel(model)

        pass




class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = StructureSmooth()
    sys.exit(app.exec_())