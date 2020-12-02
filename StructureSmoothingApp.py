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



class StructureSmooth(QWidget):
    def __init__(self):
        super().__init__()

        self.browse_button = QtWidgets.QPushButton('Browse')
        self.browse_box = QtWidgets.QLineEdit()
        self.structurePlot_box = QtWidgets.QTabWidget()
        self.analyzeStructure_button = QtWidgets.QPushButton('Analyze Structure')

        self.structurePlot_text = QtWidgets.QLabel('Current Structure')

        browse_layout = QtWidgets.QHBoxLayout()
        browse_layout.addWidget(self.browse_button)
        browse_layout.addWidget(self.browse_box)

        master_layout = QtWidgets.QVBoxLayout()
        master_layout.addLayout(browse_layout)
        master_layout.addWidget(self.structurePlot_text)
        master_layout.addWidget(self.structurePlot_box, 1)
        master_layout.addWidget(self.analyzeStructure_button)

        self.setLayout(master_layout)
        self.initUI()

        self.connect()

    def initUI(self):

        self.setGeometry(20, 55, 1100, 900)
        self.setWindowTitle('Smooooooth')

        self.show()

    def connect(self):
        self.browse_button.clicked.connect(self.browseFiles)
        self.analyzeStructure_button.clicked.connect(self.analyzeStructure)

    def browseFiles(self):

        self.folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Folder Browser")
        folder_arr = self.folder_path.strip().split('/')
        self.folder_name = folder_arr[-1]

        if self.folder_path:

            self.browse_box.clear()
            self.browse_box.insert(self.folder_path)

            file_arr = os.listdir(self.folder_path)

    def analyzeStructure(self):

        base_path = self.folder_path

        logFile_array = []

        for file in os.listdir(self.folder_path):

            if 'struct' in file.lower() and file.endswith('.csv'):
                structureVerification_path = os.path.join(base_path, file)

            if file.endswith('.txt') or file.endswith('.log'):
                logFile_array.append(file)

        log_path = os.path.join(self.folder_path, logFile_array[0])

        data = parseLogs(log_path, structureVerification_path)
        combined_data = combineTilts(data)
        writeToCSV(combined_data, base_path)
        xtilt_real, ytilt_real = formatData(combined_data)
        currentStructure_plot, newStructurePlot = recreateStructure(xtilt_real, ytilt_real)

        fig_current = plotArray(currentStructure_plot, -10, 10)
        fig_new = plotArray(newStructurePlot, -10, 10)

        fig1 = showQT(fig_current)
        fig2 = showQT(fig_new)

        self.structurePlot_box.addTab(fig1, 'Current')
        self.structurePlot_box.addTab(fig2, 'New')




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = StructureSmooth()
    sys.exit(app.exec_())
