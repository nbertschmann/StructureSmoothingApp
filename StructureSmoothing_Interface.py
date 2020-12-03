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
        self.currentLevelness_box = QtWidgets.QTabWidget()
        self.newLevelness_Box  = QtWidgets.QTabWidget()
        self.analyzeStructure_button = QtWidgets.QPushButton('Analyze Structure')

        self.currentLevelness_text = QtWidgets.QLabel('Current Structure')
        self.newLevelness_text = QtWidgets.QLabel('New Structure')

        browse_layout = QtWidgets.QHBoxLayout()
        browse_layout.addWidget(self.browse_button)
        browse_layout.addWidget(self.browse_box)

        master_layout = QtWidgets.QVBoxLayout()
        master_layout.addLayout(browse_layout)
        master_layout.addWidget(self.currentLevelness_text)
        master_layout.addWidget(self.currentLevelness_box)
        master_layout.addWidget(self.newLevelness_text)
        master_layout.addWidget(self.newLevelness_Box)
        master_layout.addWidget(self.analyzeStructure_button)

        self.setLayout(master_layout)
        self.initUI()

        self.connect()

    def initUI(self):

        self.setGeometry(50, 75, 1000, 900)
        self.setWindowTitle('Smooooooth')

        self.show()

    def connect(self):
        self.browse_button.clicked.connect(self.browseFiles)

    def browseFiles(self):

        self.folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Folder Browser")
        folder_arr = self.folder_path.strip().split('/')
        self.folder_name = folder_arr[-1]

        if self.folder_path:

            self.browse_box.clear()
            self.browse_box.insert(self.folder_path)

            file_arr = os.listdir(self.folder_path)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = StructureSmooth()
    sys.exit(app.exec_())
