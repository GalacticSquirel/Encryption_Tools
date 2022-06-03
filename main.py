import argparse
from base64 import urlsafe_b64decode as b64d, urlsafe_b64encode as b64e
import json
import math
from multiprocessing.pool import ThreadPool
import os
import os
import sys
import zlib

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QPauseAnimation, Qt
from PyQt6.QtCore import QSize, Qt, QTimer,QPoint, QEasingCurve, QPoint, QPoint, QPropertyAnimation, QSequentialAnimationGroup
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import *

import bcrypt
from cryptography.fernet import Fernet
from tqdm import tqdm



class encrypt_decrypt():

    def write_key(self):

        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)

    def load_key(self):
        
        return open("key.key", "rb").read()


    def encrypt(self,filename, key):
        
        f = Fernet(key)
        with open(filename, "rb") as file:
            file_data = file.read()

        encrypted_data = f.encrypt(file_data)
        
        with open(filename, "wb") as file:
            file.write(encrypted_data)


    def decrypt(self,filename, key):

        f = Fernet(key)
        with open(filename, "rb") as file:
            encrypted_data = file.read()
            
        decrypted_data = f.decrypt(encrypted_data)
        
        with open(filename, "wb") as file:
            file.write(decrypted_data)


    def crypt(self,eord,file):
        

            if eord == True:
                self.encrypt(file,self.load_key())
            else:
                self.decrypt(file,self.load_key())

    def run(self,directory,saltyness,eord):
        fi = []
        for path, subdirs, files in os.walk(directory):
            try:
                for name in files:
                    fi.append(os.path.join(path, name))
            except:
                pass

        fi = fi*saltyness

        def update_progress_bar(result):
            progress_bar.update(1)
            
        global progress_bar
        p = ThreadPool(len(fi))
        with tqdm(total=len(fi)) as progress_bar:
            for f in fi:
                p.apply_async(self.crypt, args=(eord,f,), callback=update_progress_bar)
            p.close()
            p.join()

def pass_deduction(pass_):
    def obscure(data: bytes) -> bytes:
        return b64e(zlib.compress(data, 9))
    
    text= pass_ * 7
    obscured = (obscure(text.encode("utf-8")))
    print(obscured.decode("utf-8"))
    total = 1
    mord = True
    for l in list(obscured):

        if mord == True:
            total = total * l
            mord = False
        else:
            total = total + l
            mord = True

    d = (int(str(round(float(str(total/len(text)).split("e")[0]),0)).strip(".0")))

    while  d > 5:
        d = math.trunc((d / (int(len(str(d)) + len(text))))*1.5)

    if d == 0:
        d = math.trunc(obscured[0]/15)
        
    return d

# e = encrypt_decrypt()

# parser = argparse.ArgumentParser(description="Simple Directory Encryptor Script")

# parser.add_argument("directory", help="Directory to encrypt/decrypt")

# parser.add_argument("passcode", help="Passcode to encrypt/decrypt with")

# parser.add_argument("-g", "--generate-key", dest="generate_key", action="store_true", help="Whether to generate a new key or use existing")

# parser.add_argument("-e", "--encrypt", action="store_true", help="Whether to encrypt the directory, only -e or -d can be specified.")

# parser.add_argument("-d", "--decrypt", action="store_true", help="Whether to decrypt the directory, only -e or -d can be specified.")

# args = parser.parse_args()
# directory = args.directory
# generate_key = args.generate_key
# into = args.passcode

# saltyness = pass_deduction(into)

# if generate_key:
#     e.write_key()

# encrypt_ = args.encrypt
# decrypt_ = args.decrypt

# if encrypt_ and decrypt_:
#     raise TypeError("Please specify whether you want to encrypt the files or decrypt it.")
# elif encrypt_:
#     e.run(directory, saltyness, True)
# elif decrypt_:
#     e.run(directory, saltyness, False)
# else:
#     raise TypeError("Please specify whether you want to encrypt the files or decrypt it.")




app = QApplication(sys.argv)
with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
        





# Todo: create a index of all encrypted locations with encrypted passw for each one in dictionary file
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(500, 470))
        self.setWindowTitle("Encryption Tool")
        
        self.UiComponents()



    def UiComponents(self):    

        self.alert_label = QLabel("", self)
        self.alert_label.setGeometry(0, -20, 500, 20)
        self.alert_label.setStyleSheet("")
        self.alert_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
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
        
        self.passcode = QLineEdit("",self)
        self.passcode.setGeometry(140, 220, 220, 32)
        self.passcode.setMaxLength(20)

        
        self.encrypt = QPushButton('Encrypt', self)
        self.encrypt.setStyleSheet("font-size: 13px;")
        self.encrypt.setGeometry(260,300,180,55)
        self.encrypt.clicked.connect(self.encrypt_pressed)
        
        self.decrypt = QPushButton('Decrypt', self)
        self.decrypt.setStyleSheet("font-size: 13px;")
        self.decrypt.setGeometry(60,300,180,55)
        self.decrypt.clicked.connect(self.decrypt_pressed)

    def alert(self, message):
        print(message)

        self.encrypt.setEnabled(False)
        QTimer.singleShot(8000, lambda: self.encrypt.setDisabled(False))
        self.decrypt.setEnabled(False)
        QTimer.singleShot(8000, lambda: self.decrypt.setDisabled(False))
        
        x = self.alert_label.x()
        y = self.alert_label.y()
        if x == 0 and y == -20:
            print("Start")
            self.alert_label.setText(message)

            self.alert_label.setStyleSheet("background-color: red;"
                                            "font-size: 18px;")

            self.anim = QPropertyAnimation(self.alert_label, b"pos") # pyright: ignore
            self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
            self.anim.setEndValue(QPoint(0, 0))
            self.anim.setDuration(1500)
            self.anim_2 = QPropertyAnimation(self.alert_label, b"pos") # pyright: ignore
            self.anim_2.setEndValue(QPoint(0, -20))
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
        print(dir_)
        n = ("Selected:  " + dir_).split("/")
        
        for part in n:
            if n.index(part) == len(n):
                print("end")
            if len(part) > 12 and not ":" in part and not n.index(part) == len(n)-1:
                n[n.index(part)]= "..."

        while len("\\".join(n)) > 70:
            del n[1]
            
        n.insert(1,"...")
        self.select_label.setText("\\".join(n))
        
        self.directory = dir_
        
    def encrypt_pressed(self):
    # Todo: check if empty
        print(self.passcode.text())
        
        hashed = bcrypt.hashpw(self.passcode.text().encode("utf-8"), bcrypt.gensalt(10))
        with open("passw", "wb") as f:
            f.write(hashed)
            f.close()
        #e = encrypt_decrypt()
        #e.run(self.directory, pass_deduction(self.passcode.text()), True)
    def decrypt_pressed(self):

        self.alert("No Folder Selected")

        if bcrypt.checkpw(self.passcode.text().encode("utf-8"),open("passw", "rb").read()):

            print("correct")
        else:
            print("failed")
    

app.setStyle("Fusion")


window = MainWindow()
window.show()
app.exec()

