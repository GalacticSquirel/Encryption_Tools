import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import * # pyright: ignore[reportWildcardImportFromLibrary]
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QSize, Qt
import time
import os
import textwrap

app = QApplication(sys.argv)
with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
        
                
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(500, 470))
        self.setWindowTitle("Encryption Tool")
        
        self.UiComponents()

    def UiComponents(self):    
        
        self.select = QPushButton("Select Folder",self)
        self.select.setGeometry(140, 30, 220, 48)

        self.select.clicked.connect(self.select_folder)
        
        self.select_label = QLabel("No Folder Selected Yet", self)
        self.select_label.setGeometry(10, 85, 480, 45)
        self.select_label.setStyleSheet("font-size: 3vw;")
        self.select_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.passcode_label = QLabel("Enter Passphrase For Encryption:", self)
        self.passcode_label.setGeometry(140, 166, 220, 32)
        self.passcode_label.setStyleSheet("font-size: 15px;")
        self.passcode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.passcode = QLineEdit("Passphrase",self)
        self.passcode.setGeometry(140, 220, 220, 32)
        
        self.encrypt = QPushButton('Encrypt', self)
        self.encrypt.setStyleSheet("font-size: 13px;")
        self.encrypt.setGeometry(260,300,180,55)
        
        self.decrypt = QPushButton('Decrypt', self)
        self.decrypt.setStyleSheet("font-size: 13px;")
        self.decrypt.setGeometry(60,300,180,55)
        
        
    def select_folder(self):
        dir_ = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select project folder:')

        n = ("Selected:  " + dir_).split("/")
        for part in n:
            if len(part) > 12 and not ":" in part:
                n[n.index(part)]= "..."
        
        print(n)
        while len("\\".join(n)) > 70:
            del n[1]
            
        n.insert(1,"...")
        self.select_label.setText("\\".join(n))
        self.directory = dir_
        
        



app.setStyle("Fusion")


window = MainWindow()
window.show()
app.exec()

