import argparse
from base64 import urlsafe_b64decode as b64d, urlsafe_b64encode as b64e
import json
import math
from multiprocessing.pool import ThreadPool
import os
import os
import sys
import zlib
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QPauseAnimation, Qt
from PyQt6.QtCore import (
    QEasingCurve,
    QPoint,
    QPoint,
    QPoint,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    QSize,
    QTimer,
    Qt,
)
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import * # pyright: ignore
import bcrypt
from cryptography.fernet import Fernet

from pathlib import Path





app = QApplication(sys.argv)
with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
        





# Todo: create a index of all encrypted locations with encrypted passw for each one in dictionary file

#Todo: button to generate new key
#Todo: random passcode maybe 
#Todo: custom top bar
#Todo: encrypt key.key with passcode
#Todo: rename files within directory to encrypted names
#Todo: remove deduduction 

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Encryption Tool")
        #self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        #self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.UiComponents()

        self.proceed_folder = False
        self.proceed_passphrase = False
        #self.setMouseTracking(True)

        # transparency cannot be set for window BG in style sheets, so...
        # self.setWindowOpacity(0.1) 
        # self.setWindowFlags(
        #         QtCore.Qt.WindowType.FramelessWindowHint # hides the window controls
        #         | QtCore.Qt.WindowType.WindowStaysOnTopHint # forces window to top... maybe
        #         | QtCore.Qt.WindowType.SplashScreen # this one hides it from the task bar!
        #         )
        # alternative way of making base window transparent
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True) #100% transparent
    def write_key(self):

        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)

    def load_key(self):
        
        return open("key.key", "rb").read()


    def encrypt(self, filename, key):
        
        f = Fernet(key)
        with open(filename, "rb") as file:
            file_data = file.read()

        encrypted_data = f.encrypt(file_data)
        
        with open(filename, "wb") as file:
            file.write(encrypted_data)


    def decrypt(self, filename, key):

        f = Fernet(key)
        with open(filename, "rb") as file:
            encrypted_data = file.read()
            
        decrypted_data = f.decrypt(encrypted_data)
        
        with open(filename, "wb") as file:
            file.write(decrypted_data)


    def crypt(self, eord,file):
        
        self.value = self.value +1
        if eord == True:
            
            print(self.value)
            print("e ", file)
            self.encrypt(file, self.load_key())
        else:
            self.decrypt(file, self.load_key())

    def run(self, directory,saltyness,eord):

        print(directory)
        print(saltyness)
        print(eord)
        self.fi = []
        for path, subdirs, files in os.walk(directory):
            try:
                for name in files:
                    self.fi.append(os.path.join(path, name))
            except:
                pass
        self.prog_bar.setRange(0, len(self.fi))
        self.fi = self.fi*int(saltyness)

        # def update_progress_bar(result):
        #     value = self.prog_bar.value()
        #     self.prog_bar.setValue(value + 1)
            
        # global progress_bar
        # p = ThreadPool(len(fi))

        # for f in fi:
        #     p.apply_async(self.crypt, args=(eord,f,), callback=update_progress_bar)
        # p.close()
        # p.join()
        
        middle_index=round(len(self.fi)/2)

        first_half=self.fi[:middle_index]
        sec_half=self.fi[middle_index:]
        
        self.value = 0
        with ThreadPoolExecutor(round(len(first_half))) as executor:
            futures = []
            for i in first_half:
                print(i)
                futures.append(executor.submit(lambda:self.crypt(eord,i)))
            for future in as_completed(futures):
                self.prog_bar.setValue(self.value)
                
        with ThreadPoolExecutor(round(len(sec_half))) as executor:
            futures = []
            for i in sec_half:
                futures.append(executor.submit(lambda:self.crypt(eord,i)))
            for future in as_completed(futures):
                self.prog_bar.setValue(self.value)


    def UiComponents(self):    

        spacing = 25
        
        self.alert_label = QLabel("", self)
        self.alert_label.setGeometry(0, -30, 500, 30)
        self.alert_label.setStyleSheet("")
        self.alert_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        self.select = QPushButton("Select Folder",self)
        self.select.setGeometry(140, 40, 220, 55)
        self.select.clicked.connect(self.select_folder)
        
        self.select_label = QLabel("No Folder Selected Yet", self)
        self.select_label.setGeometry(10, 95 + spacing, 480, 45)
        self.select_label.setStyleSheet("font-size: 3vw;")
        self.select_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.passcode_label = QLabel("Enter Passphrase For Encryption:", self)
        self.passcode_label.setGeometry(140, 140 + (spacing * 2) , 220, 30)
        self.passcode_label.setStyleSheet("font-size: 15px;")
        self.passcode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.passcode = QLineEdit("",self)
        self.passcode.setGeometry(140, 170 + (spacing * 3), 220, 30)
        self.passcode.setMaxLength(20)
        self.passcode.setEchoMode(QLineEdit.EchoMode.Password)
        self.passcode.textChanged.connect(self.line_edited)
        
        self.button = QPushButton('', self)
        self.button.setGeometry(330, 170 + (spacing * 3), 30, 30)
        self.button.clicked.connect(self.show_pass)
        self.button.setIcon(QtGui.QIcon('eye.png'))
        self.button.setIconSize(QtCore.QSize(20,30))
        self.button.setCheckable(True)
        
        self.slider_label = QLabel("Level Of Encryption:", self)
        self.slider_label.setGeometry(60, 198 + (spacing * 4), 160, 30)
        self.slider_label.setStyleSheet("font-size: 15px;")
        self.slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.slider_num = QLabel("1", self)
        self.slider_num.setGeometry(410, 198 + (spacing * 4), 20, 30)
        self.slider_num.setStyleSheet("font-size: 15px;")
        self.slider_num.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.slider.setGeometry(240, 200 + (spacing * 4), 160, 30)
        self.slider.valueChanged[int].connect(self.slider_update) #pyright: ignore
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
    
        self.encrypt_button = QPushButton('Encrypt', self)
        self.encrypt_button.setStyleSheet("font-size: 13px;")
        self.encrypt_button.setGeometry(260, 230 + (spacing * 5),180,55)
        self.encrypt_button.clicked.connect(self.encrypt_pressed)
        self.encrypt_button.setDisabled(True)
        
        self.decrypt_button = QPushButton('Decrypt', self)
        self.decrypt_button.setStyleSheet("font-size: 13px;")
        self.decrypt_button.setGeometry(60, 230 + (spacing * 5),180,55)
        self.decrypt_button.clicked.connect(self.decrypt_pressed)
        self.decrypt_button.setDisabled(True)
        
        self.prog_bar = QProgressBar(self)
        self.prog_bar.setGeometry(60, 285 + (spacing * 6), 380, 55)
        
        mx = 380 + (spacing * 6)
        self.setFixedSize(QSize(500, mx))

    # def mousePressEvent(self, e):
    #     print("mousePressEvent")
    #     x = int(e.position().x())
    #     y = int(e.position().y())
    #     print(x,y)
        
    # def mouseReleaseEvent(self, e):
    #     print("mouseReleaseEvent")
    def alert(self, message,severity):
        print(message)
        # self.encrypt.setEnabled(False)
        # QTimer.singleShot(8000, lambda: self.encrypt.setDisabled(False))
        # self.decrypt.setEnabled(False)
        # QTimer.singleShot(8000, lambda: self.decrypt.setDisabled(False))
        if severity == 0:
            color = "red"
        elif severity == 1:
            color = "#ffbf00"
        elif severity == 2:
            color = "green"
        else:
            color = "red"

        x = self.alert_label.x()
        y = self.alert_label.y()
        if x == 0 and y == -30:
            self.alert_label.setText(message)
            self.alert_label.setStyleSheet(f"background-color: {color};"
                                            "font-size: 16px;")
            self.anim = QPropertyAnimation(self.alert_label, b"pos") # pyright: ignore
            self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
            self.anim.setEndValue(QPoint(0, 0))
            self.anim.setDuration(1500)
            self.anim_2 = QPropertyAnimation(self.alert_label, b"pos") # pyright: ignore
            self.anim_2.setEndValue(QPoint(0, -30))
            self.anim_2.setDuration(2000)
            self.delay = QPauseAnimation(5000)
            self.anim_group = QSequentialAnimationGroup()
            self.anim_group.addAnimation(self.anim)
            self.anim_group.addAnimation(self.delay)
            self.anim_group.addAnimation(self.anim_2)
            
            self.anim_group.start()
        else:
            self.return_ = QPropertyAnimation(self.alert_label, b"pos") # pyright: ignore
            self.return_.setEndValue(QPoint(0, -20))
            self.return_.setDuration(1000)
            self.return_.start()

    def select_folder(self):
        dir_ = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select project folder:')
        
        con = True
        parent_path_to_test = dir_
        child_path_to_test = os.path.dirname(os.path.realpath(__file__))
        try:
            if os.path.commonpath([os.path.abspath(parent_path_to_test)]) == os.path.commonpath([os.path.abspath(parent_path_to_test), os.path.abspath(child_path_to_test)]):
                con = False
        except ValueError:
            con = True

        if con == True:            
            if not len(dir_) == 3:
                n = ("Selected:  " + dir_).split("/")
                for part in n:
                    if n.index(part) == len(n):
                        print("end")
                    if len(part) > 15 and not ":" in part and not n.index(part) == len(n)-1:
                        n[n.index(part)]= "..."

                while len("\\".join(n)) > 70:
                    del n[1]
                    
                n.insert(1,"...")
                n = "\\".join(n)
            else:
                n = dir_
                print("root")
                print(n)
                self.alert("You have selected a disk", 1)
                
            if os.access(dir_, os.R_OK | os.W_OK):
                self.directory = dir_
                print("dir ok")
                self.proceed_folder = True
                self.select_label.setText(n)
            else:
                self.alert("Please select a valid folder", 0)
                self.select_label.setText("Folder Selected Is Not Valid")
                self.proceed_folder = False
        else:
            self.alert("The directory you selected contains this program", 0)
            self.select_label.setText("Folder Selected Is Not Valid")
            self.proceed_folder = False
        self.check_for_unlock()
        
    def encrypt_pressed(self):
        print(self.passcode.text())
        self.value = 0
        self.prog_bar.setValue(self.value)
        hashed = bcrypt.hashpw(self.passcode.text().encode("utf-8"), bcrypt.gensalt(10))
        with open("passw", "wb") as f:
            f.write(hashed)
            f.close()
        #e = encrypt_decrypt()
        self.run(self.directory, self.slider_num.text(), True)
        
    def decrypt_pressed(self):

        if bcrypt.checkpw(self.passcode.text().encode("utf-8"),open("passw", "rb").read()):
            self.value = 0
            self.prog_bar.setValue(self.value)
            self.alert("Passphrase is correct", 2)
            self.run(self.directory, self.slider_num.text(), False)
        else:
            self.alert("Passphrase is not correct", 0)
    
    def line_edited(self):
        print(self.passcode.text())
        if len(self.passcode.text()) > 2:
            self.proceed_passphrase = True
        else:
            self.proceed_passphrase = False
        self.check_for_unlock()
        
    def show_pass(self):
        if self.button.isChecked():
            self.passcode.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passcode.setEchoMode(QLineEdit.EchoMode.Password)
            
    def slider_update(self, value):
        self.slider_num.setText(str(value))
        
    def check_for_unlock(self):
        if self.proceed_folder == True and self.proceed_passphrase == True:
            self.encrypt_button.setEnabled(True)
            self.decrypt_button.setEnabled(True)
        else:
            self.encrypt_button.setEnabled(False)
            self.decrypt_button.setEnabled(False)




app.setStyle("Fusion")
window = MainWindow()
window.show()
app.exec()

