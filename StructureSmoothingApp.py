from ParseLogs import parseLogs
from CombineTilts import combineTilts
from CombineTilts2 import combineTilts2
from WriteToCSV import writeToCSV
from FormatData import formatData
from RecreateStructure import recreateStructure
from PlotArray import plotArray
from ModifyPostHeights import modifyPostHeights
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
from PyQt5.QtCore import Qt, QObject
import pandas as pd

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtCore import QRunnable
import time
import traceback, sys

import plotly.graph_objects as go



class WorkerSignals(QObject):

    clearTabs = pyqtSignal()
    plotStruct = pyqtSignal(go.Figure, go.Figure)
    errorMessage = pyqtSignal(str, str)
    abortProgram = pyqtSignal()
    showProgress = pyqtSignal(int, str)

class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.kwargs['clear_tabs_callback'] = self.signals.clearTabs
        self.kwargs['plot_callback'] = self.signals.plotStruct
        self.kwargs['error_message_callback'] = self.signals.errorMessage
        self.kwargs['abort_callback'] = self.signals.abortProgram
        self.kwargs['progress_callback'] = self.signals.showProgress
    @pyqtSlot()
    def run(self):

        result = self.fn(*self.args, **self.kwargs)
        print(str(result))


class StructureSmooth(QWidget):
    def __init__(self):
        super().__init__()

        self.file_path = ''
        self.file_name = ''
        self.folder_path = ''
        self.folder_name = ''
        self.postHeight_path = ''
        self.file_arr = []

        self.global_str = ''
        self.format_str = ''
        self.combineTilts_str = ''
        self.recreateStruct_str = ''
        self.modifyPost_str = ''

        self.setWindowIcon(QtGui.QIcon('structure3.ico'))
        self.my_layout = QtWidgets.QVBoxLayout(self)

        self.plotStructure_button = QPushButton("Create Plots")
        self.browse_button1 = QtWidgets.QPushButton('Browse')
        self.browse_box1 = QtWidgets.QLineEdit()
        self.browse_box1.setReadOnly(True)

        self.plotDisplay_tab = QtWidgets.QTabWidget()

        self.progressBox = QtWidgets.QTextEdit()

        self.browse_layout1 = QtWidgets.QHBoxLayout()
        self.browse_layout1.addWidget(self.browse_button1)
        self.browse_layout1.addWidget(self.browse_box1)

        self.tab_layout1 = QtWidgets.QVBoxLayout()
        self.tab_layout1.addLayout(self.browse_layout1)
        self.tab_layout1.addWidget(self.plotDisplay_tab,6)
        self.tab_layout1.addWidget(self.progressBox, 1)
        self.tab_layout1.addWidget(self.plotStructure_button)

        self.analyzeLogs_button = QtWidgets.QPushButton("Analyze Logs")
        self.browse_button2 = QtWidgets.QPushButton('Browse')
        self.browse_box2 = QtWidgets.QLineEdit()
        self.browse_box2.setReadOnly(True)

        self.table_display = self.initTable()

        self.browse_layout2 = QtWidgets.QHBoxLayout()
        self.browse_layout2.addWidget(self.browse_button2)
        self.browse_layout2.addWidget(self.browse_box2)

        self.tree = self.init_FileViewer()

        self.tab_layout2 = QtWidgets.QVBoxLayout()
        self.tab_layout2.addLayout(self.browse_layout2)
        self.tab_layout2.addWidget(self.tree, 1)
        self.tab_layout2.addWidget(self.table_display,3)
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

        self.disableButtons()
        self.initUI()
        self.connect()
        self.threadpool = QThreadPool()

    def disableButtons(self):

        self.analyzeLogs_button.setDisabled(True)
        self.plotStructure_button.setDisabled(True)

    def initTable(self):

        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['DM', 'X', 'Y', 'Z', 'Pitch', 'Roll'])

        self.table = QtWidgets.QTableView()

        # font = QtGui.QFont()
        # font.setBold(True)
        #
        # self.table.horizontalHeader().setFont(font)
        # self.table.verticalHeader().setFont(font)

        self.table.setModel(model)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)

        return self.table

    def init_FileViewer(self):
        self.model = QtWidgets.QFileSystemModel()



        tree = QtWidgets.QTreeView()
        tree.setModel(self.model)
        tree.setAlternatingRowColors(True)

        font = QtGui.QFont()
        font.setBold(True)

        header = tree.header()
        # header.setFont(font)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        tree.setColumnWidth(0, 350)

        return tree

    def set_FileViewer(self):

        self.model.setRootPath(self.folder_path)

        self.tree.setRootIndex(self.model.index(self.folder_path))


    def initUI(self):

        self.setGeometry(50, 75, 1000, 900)
        self.setWindowTitle(' Structure Smoothing Application')

        self.show()

    def connect(self):
        self.browse_button1.clicked.connect(self.browseFiles1)
        self.browse_button2.clicked.connect(self.browseFiles2)
        self.analyzeLogs_button.clicked.connect(self.analyzeLogs)
        self.plotStructure_button.clicked.connect(self.start)

    def browseFiles1(self):

        file_path_tuple = QtWidgets.QFileDialog.getOpenFileName(self, "File Browser")

        self.file_path = file_path_tuple[0]
        file_array = self.file_path.strip().split('/')
        self.file_name = file_array[-1]

        if self.file_path:

            self.browse_box1.clear()
            self.browse_box1.insert(self.file_path)
            self.plotStructure_button.setEnabled(True)

            temp_folder = os.path.split(self.file_path)
            self.postHeight_path = temp_folder[0]

        pass

    def browseFiles2(self):

        self.folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Folder Browser")

        folder_arr = self.folder_path.strip().split('/')
        self.folder_name = folder_arr[-1]

        if self.folder_path:
            self.browse_box2.clear()
            self.browse_box2.insert(self.folder_path)
            self.file_arr = os.listdir(self.folder_path)

            self.analyzeLogs_button.setEnabled(True)
            self.set_FileViewer()


    def analyzeLogs(self):

        log_array = []
        df_array = []
        logDataRaw_name = 'logDataRaw.csv'
        logDataCombined_name = 'logDataCombined.csv'
        structureVerfication_file = ''
        output_path = os.path.join(self.folder_path, 'output')

        if not os.path.exists(output_path):
            os.mkdir(output_path)

        for file in self.file_arr:
            if 'tblStruct' in file:
                structureVerfication_file = os.path.join(self.folder_path, file)
            if 'auto_output' in file:
                log_array.append(file)

        # if any of the required files are not present
        error_list = []
        if not structureVerfication_file:
            error_list.append("Structure Verification file")
        if not log_array:
            error_list.append("Log file")
        if error_list:
            error_str = ', '.join(error_list)

            self.showErrorMessage('Error', 'Files Missing: ' + error_str)
            return 0

        for file in log_array:
            log_path = os.path.join(self.folder_path, file)
            log_data = parseLogs(log_path, structureVerfication_file)
            df_array.append(log_data)

        log_data_raw = pd.concat(df_array)
        log_data_combined = combineTilts2(log_data_raw)

        font = QtGui.QFont()
        font.setBold(True)

        self.table.horizontalHeader().setFont(font)
        self.table.verticalHeader().setFont(font)

        model = TableModel(log_data_combined)

        self.table_display.setModel(model)

        writeToCSV(log_data_raw, output_path, logDataRaw_name)
        writeToCSV(log_data_combined, output_path, logDataCombined_name)

    def plotStructure(self, clear_tabs_callback, plot_callback, error_message_callback, abort_callback, progress_callback):

        clear_tabs_callback.emit()
        postHeight_file = 'postHeights.csv'

        if self.file_path.endswith('.csv'):

            try:
                structureData_raw = pd.read_csv(self.file_path, usecols=['DM', 'X', 'Y', 'Z', 'Pitch', 'Roll'])
            except Exception as exp:
                print('[ERROR]', exp)

                title = 'Column Error'
                message = 'Input File ' + '\'' + self.file_name + '\'' + ' does not have correct number of columns for analysis [DM, X, Y, Z, Pitch, Roll]'

                error_message_callback.emit(title, message)
                abort_callback.emit()

                return 0

        else:

            title = 'File Type Error'
            message = 'Input File ' + '\'' + self.file_name + '\'' + ' is not an acceptable file type. File must end with \'.csv\''
            error_message_callback.emit(title, message)
            abort_callback.emit()


            return 0

        structureData = combineTilts(structureData_raw, progress_callback)

        xtilt_real, ytilt_real = formatData(structureData, progress_callback)

        Zheight_recreated, Zheight_lowpass, Zheight_delta = recreateStructure(xtilt_real, ytilt_real, progress_callback)

        postHeight_data = modifyPostHeights(Zheight_delta)

        writeToCSV(postHeight_data, self.postHeight_path, postHeight_file)

        currentStructure_plot = plotArray(Zheight_recreated, -30, 30)
        newStructure_plot = plotArray(Zheight_lowpass, -30, 30)

        progress_callback.emit(4, 'Generating Plots...')
        plot_callback.emit(currentStructure_plot, newStructure_plot)

        pass

    def plotIt(self, currentStructure_plot, newStructure_plot):

        print("Plot Function")
        currentStructure_html = showQT(currentStructure_plot)
        newStructure_html = showQT(newStructure_plot)

        self.plotDisplay_tab.addTab(currentStructure_html, 'Current Structure')
        self.plotDisplay_tab.addTab(newStructure_html, 'New Structure')

        self.plotStructure_button.setEnabled(True)
        # self.progressBox.append('Plotting Complete')

        print("Done Plotting")

    def start(self):

        # Pass the function to execute
        worker = Worker(self.plotStructure)  # Any other args, kwargs are passed to the run function

        worker.signals.clearTabs.connect(self.clearPlotTabs)
        worker.signals.plotStruct.connect(self.plotIt)
        worker.signals.errorMessage.connect(self.showErrorMessage)
        worker.signals.abortProgram.connect(self.abortNow)
        worker.signals.showProgress.connect(self.progress)

        self.threadpool.start(worker)


    def progress(self, progress_type, progress_str):
        # print("Progress: " + progress_str)


        if progress_type == 0:

            self.format_str = progress_str
            self.global_str = self.format_str
            self.progressBox.setText(self.global_str)

        if progress_type == 1:
            self.combineTilts_str = progress_str
            self.global_str = self.format_str + '\n' + self.combineTilts_str
            self.progressBox.setText(self.global_str)

        if progress_type == 2:
            self.recreateStruct_str = progress_str
            self.global_str = self.format_str + '\n' + self.combineTilts_str + '\n' + self.recreateStruct_str
            self.progressBox.setText(self.global_str)

        if progress_type == 3:
            self.modifyPost_str = progress_str
            self.global_str = self.format_str + '\n' + self.combineTilts_str + '\n' + self.recreateStruct_str + '\n' + self.modifyPost_str
            self.progressBox.setText(self.global_str)

        if progress_type == 4:
            self.global_str = self.global_str = self.format_str + '\n' + self.combineTilts_str + '\n' + self.recreateStruct_str + '\n' + self.modifyPost_str + '\n' + progress_str
            self.progressBox.setText(self.global_str)

    def abortNow(self):

        self.plotStructure_button.setEnabled(True)

    def clearPlotTabs(self):

        self.plotDisplay_tab.clear()
        self.progressBox.clear()
        self.plotStructure_button.setDisabled(True)

    def showErrorMessage(self, title, error_message):
        msg = QtWidgets.QMessageBox()

        pos_X = float(self.pos().x())
        pos_Y = float(self.pos().y())

        height = float(self.size().height())
        width = float(self.size().width())

        errorBoxPos_X = pos_X + width/2 - 250
        errorBoxPos_Y = pos_Y + height/2

        msg.setGeometry(int(errorBoxPos_X), int(errorBoxPos_Y),300, 200)

        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(error_message)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()


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