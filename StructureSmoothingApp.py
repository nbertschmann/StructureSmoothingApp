from ParseLogs import parseLogs
from CombineTilts import combineTilts
from CombineTilts2 import combineTilts2
from WriteToCSV import writeToCSV
from FormatData import formatData
from RecreateStructure import recreateStructure
from PlotArray import plotArray
from ModifyPostHeights import modifyPostHeights
from ShowQT import showQT
from NormalizeTilts import normalizeTilts

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

    # Signals for structure plotting
    clearTabs1 = pyqtSignal()
    plotStruct1 = pyqtSignal(go.Figure, go.Figure)
    errorMessage1 = pyqtSignal(str, str)
    abortProgram1 = pyqtSignal()
    showProgress1 = pyqtSignal(int, str)
    begin1 = pyqtSignal()
    finish1 = pyqtSignal()

    # Signals for log parsing/display
    clearTable2 = pyqtSignal()
    displayTable2 = pyqtSignal(pd.DataFrame)
    errorMessage2 = pyqtSignal(str, str)
    abortProgram2 = pyqtSignal()
    showProgress2 = pyqtSignal(int, str)
    begin2 = pyqtSignal()
    finish2 = pyqtSignal()




class Worker1(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker1, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.kwargs['clear_tabs_callback'] = self.signals.clearTabs1
        self.kwargs['plot_callback'] = self.signals.plotStruct1
        self.kwargs['error_message_callback'] = self.signals.errorMessage1
        self.kwargs['abort_callback'] = self.signals.abortProgram1
        self.kwargs['progress_callback'] = self.signals.showProgress1
        self.kwargs['begin_callback'] = self.signals.begin1
        self.kwargs['finish_callback'] = self.signals.finish1


    @pyqtSlot()
    def run(self):

        result = self.fn(*self.args, **self.kwargs)
        print(str(result))



class Worker2(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker2, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.kwargs['clear_table_callback'] = self.signals.clearTable2
        self.kwargs['display_table_callback'] = self.signals.displayTable2
        self.kwargs['error_message_callback'] = self.signals.errorMessage2
        self.kwargs['abort_callback'] = self.signals.abortProgram2
        self.kwargs['progress_callback'] = self.signals.showProgress2
        self.kwargs['begin_callback'] = self.signals.begin2
        self.kwargs['finish_callback'] = self.signals.finish2

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
        self.bold_font = QtGui.QFont()
        self.bold_font.setBold(True)

        # ********************************************** Tab 1 Layout **************************************************
        self.my_layout = QtWidgets.QVBoxLayout(self)

        self.plotStructure_button = QPushButton("Create Plots")
        self.browse_button1 = QtWidgets.QPushButton('Browse')
        self.browse_box1 = QtWidgets.QLineEdit()
        self.browse_box1.setReadOnly(True)

        self.location_label = QtWidgets.QLabel('    Location')
        self.location_label.setFont(self.bold_font)
        self.secret_label = QtWidgets.QLabel('')
        self.location_comboBox = QtWidgets.QComboBox()

        self.location_comboBox.addItem('Basement')
        self.location_comboBox.addItem('Attic')
        self.location_comboBox.addItem('Attic + Basement ')
        self.location_comboBox.setCurrentIndex(-1)

        self.location_layout = QtWidgets.QHBoxLayout()
        self.location_layout.addWidget(self.location_label, 1)
        self.location_layout.addWidget(self.location_comboBox, 9)

        self.progressBar1 = QtWidgets.QProgressBar()
        self.progressBar1.setValue(0)
        self.progressLabel1 = QtWidgets.QLabel()

        self.plotDisplay_tab = QtWidgets.QTabWidget()

        self.browse_layout1 = QtWidgets.QHBoxLayout()
        self.browse_layout1.addWidget(self.browse_button1)
        self.browse_layout1.addWidget(self.browse_box1)

        self.tab_layout1 = QtWidgets.QVBoxLayout()
        self.tab_layout1.addLayout(self.browse_layout1)
        self.tab_layout1.addLayout(self.location_layout)
        self.tab_layout1.addWidget(self.plotDisplay_tab, 6)
        self.tab_layout1.addWidget(self.progressLabel1)
        self.tab_layout1.addWidget(self.progressBar1)
        self.tab_layout1.addWidget(self.plotStructure_button)

        # ********************************************** Tab 2 Layout **************************************************
        self.analyzeLogs_button = QtWidgets.QPushButton("Analyze Logs")
        self.browse_button2 = QtWidgets.QPushButton('Browse')
        self.browse_box2 = QtWidgets.QLineEdit()
        self.browse_box2.setReadOnly(True)

        self.table_display = self.initTable()

        self.browse_layout2 = QtWidgets.QHBoxLayout()
        self.browse_layout2.addWidget(self.browse_button2)
        self.browse_layout2.addWidget(self.browse_box2)

        self.progressBar2 = QtWidgets.QProgressBar()
        self.progressBar2.setValue(0)

        self.progressLabel2 = QtWidgets.QLabel()

        self.tree = self.init_FileViewer()

        self.tab_layout2 = QtWidgets.QVBoxLayout()
        self.tab_layout2.addLayout(self.browse_layout2)
        self.tab_layout2.addWidget(self.tree, 1)
        self.tab_layout2.addWidget(self.table_display, 3)
        self.tab_layout2.addWidget(self.progressLabel2)
        self.tab_layout2.addWidget(self.progressBar2)
        self.tab_layout2.addWidget(self.analyzeLogs_button)

        # *********************************************** Creating Tabs ************************************************
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

        self.table.setModel(model)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)

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
        self.plotStructure_button.clicked.connect(self.start1)
        self.analyzeLogs_button.clicked.connect(self.start2)
        self.location_comboBox.currentIndexChanged.connect(self.comboBoxSelected)

    def browseFiles1(self):

        file_path_tuple = QtWidgets.QFileDialog.getOpenFileName(self, "File Browser")

        self.file_path = file_path_tuple[0]
        file_array = self.file_path.strip().split('/')
        self.file_name = file_array[-1]

        if self.file_path:

            self.browse_box1.clear()
            self.browse_box1.insert(self.file_path)


            temp_folder = os.path.split(self.file_path)
            self.postHeight_path = temp_folder[0]

            if self.location_comboBox.currentIndex() != -1:

                self.plotStructure_button.setEnabled(True)
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

    def comboBoxSelected(self):

        if self.browse_box1.text() != '':

            self.plotStructure_button.setEnabled(True)


    def analyzeLogs(self, clear_table_callback ,display_table_callback, error_message_callback, abort_callback, progress_callback, begin_callback ,finish_callback):

        begin_callback.emit()
        clear_table_callback.emit()

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

            error_message_callback.emit('Error', 'Files Missing: ' + error_str)
            abort_callback.emit()
            return 0

        for log_ct, file in enumerate(log_array):

            log_total = len(log_array)

            log_path = os.path.join(self.folder_path, file)
            log_data = parseLogs(log_path, structureVerfication_file,  log_ct, log_total, progress_callback)
            df_array.append(log_data)

        log_data_raw = pd.concat(df_array)

        # log_data_normalized = normalizeTilts(log_data_raw)
        log_data_combined = combineTilts2(log_data_raw)

        display_table_callback.emit(log_data_combined)

        finish_callback.emit()
        writeToCSV(log_data_raw, output_path, logDataRaw_name)
        writeToCSV(log_data_combined, output_path, logDataCombined_name)


    def showTable(self, data):

        font = QtGui.QFont()
        font.setBold(True)

        self.table.horizontalHeader().setFont(font)
        self.table.verticalHeader().setFont(font)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)

        model = TableModel(data)

        self.table_display.setModel(model)

        if len(data) != 0:
            self.progressLabel2.setText('Complete.')


    def plotStructure(self, clear_tabs_callback, plot_callback, error_message_callback, abort_callback, progress_callback, begin_callback, finish_callback):

        begin_callback.emit()
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

        length = len(structureData_raw)

        if len(structureData_raw) == 0:

            title = 'File Error'
            message = 'Input File ' + '\'' + self.file_name + '\'' + ' does not contain any data'
            error_message_callback.emit(title, message)
            abort_callback.emit()
            return 0

        location = self.location_comboBox.currentText()




        structureData = combineTilts(structureData_raw, location, progress_callback)

        xtilt_real, ytilt_real = formatData(structureData, structureData_raw, progress_callback)

        Zheight_recreated, Zheight_lowpass, Zheight_delta = recreateStructure(xtilt_real, ytilt_real, progress_callback)

        postHeight_data = modifyPostHeights(Zheight_delta)

        writeToCSV(postHeight_data, self.postHeight_path, postHeight_file)

        currentStructure_plot = plotArray(Zheight_recreated, -30, 30)
        newStructure_plot = plotArray(Zheight_lowpass, -30, 30)

        plot_callback.emit(currentStructure_plot, newStructure_plot)
        finish_callback.emit()

    def plotIt(self, currentStructure_plot, newStructure_plot):

        print("Plot Function")
        currentStructure_html = showQT(currentStructure_plot)
        newStructure_html = showQT(newStructure_plot)

        self.plotDisplay_tab.addTab(currentStructure_html, 'Current Structure')
        self.plotDisplay_tab.addTab(newStructure_html, 'New Structure')

        self.plotStructure_button.setEnabled(True)

        self.progressLabel1.setText('Complete.')



    def start1(self):

        # Pass the function to execute
        worker = Worker1(self.plotStructure)  # Any other args, kwargs are passed to the run function

        worker.signals.clearTabs1.connect(self.clearPlotTabs)
        worker.signals.plotStruct1.connect(self.plotIt)
        worker.signals.errorMessage1.connect(self.showErrorMessage)
        worker.signals.abortProgram1.connect(self.abortNow1)
        worker.signals.showProgress1.connect(self.progress1)
        worker.signals.begin1.connect(self.begin)
        worker.signals.finish1.connect(self.finish)

        self.threadpool.start(worker)

    def start2(self):

        worker = Worker2(self.analyzeLogs)

        worker.signals.displayTable2.connect(self.showTable)
        worker.signals.errorMessage2.connect(self.showErrorMessage)
        worker.signals.showProgress2.connect(self.progress2)
        worker.signals.abortProgram2.connect(self.abortNow2)
        worker.signals.clearTable2.connect(self.clearTable)
        worker.signals.begin2.connect(self.begin)
        worker.signals.finish2.connect(self.finish)

        self.threadpool.start(worker)

    def begin(self):

        self.analyzeLogs_button.setDisabled(True)
        self.browse_button2.setDisabled(True)
        self.plotStructure_button.setDisabled(True)
        self.browse_button1.setDisabled(True)
        self.location_comboBox.setDisabled(True)

    def finish(self):

        self.analyzeLogs_button.setEnabled(True)
        self.browse_button2.setEnabled(True)
        self.plotStructure_button.setEnabled(True)
        self.browse_button1.setEnabled(True)
        self.location_comboBox.setEnabled(True)

        if self.browse_box2.text() != '':
            self.analyzeLogs_button.setEnabled(True)

        if self.browse_box1.text() != '':
            self.plotStructure_button.setEnabled(True)

    def progress1(self, progress_percent, progress_str):

        self.progressLabel1.setText(progress_str)
        self.progressBar1.setValue(progress_percent)

    def progress2(self, progress_percent, progress_str):

        self.progressLabel2.setText(progress_str)
        self.progressBar2.setValue(progress_percent)

    def abortNow1(self):

        self.browse_button2.setEnabled(True)
        self.plotStructure_button.setEnabled(True)
        self.browse_button1.setEnabled(True)
        self.location_comboBox.setEnabled(True)

        if self.browse_box2.text() != '':
            self.analyzeLogs_button.setEnabled(True)

    def abortNow2(self):

        self.analyzeLogs_button.setEnabled(True)
        self.browse_button2.setEnabled(True)
        self.browse_button1.setEnabled(True)
        self.location_comboBox.setEnabled(True)

        if self.browse_box1.text() != '':
            self.plotStructure_button.setEnabled(True)

    def clearPlotTabs(self):

        self.plotDisplay_tab.clear()
        self.progressBar1.setValue(0)

    def clearTable(self):

        column_names = ['DM', 'X', 'Y', 'Z', 'Pitch', 'Roll', 'Bot']
        df = pd.DataFrame(columns=column_names)
        self.showTable(df)

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