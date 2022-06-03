import argparse
from base64 import urlsafe_b64decode as b64d, urlsafe_b64encode as b64e
import math
from multiprocessing.pool import ThreadPool
import os
import zlib

from cryptography.fernet import Fernet # pyright: ignore
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

def pass_deduction(ind):
    def obscure(data: bytes) -> bytes:
        return b64e(zlib.compress(data, 9))
    
    text= ind * 7
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

e = encrypt_decrypt()

parser = argparse.ArgumentParser(description="Simple Directory Encryptor Script")

parser.add_argument("directory", help="Directory to encrypt/decrypt")

parser.add_argument("passcode", help="Passcode to encrypt/decrypt with")

parser.add_argument("-g", "--generate-key", dest="generate_key", action="store_true", help="Whether to generate a new key or use existing")

parser.add_argument("-e", "--encrypt", action="store_true", help="Whether to encrypt the directory, only -e or -d can be specified.")

parser.add_argument("-d", "--decrypt", action="store_true", help="Whether to decrypt the directory, only -e or -d can be specified.")

args = parser.parse_args()
directory = args.directory
generate_key = args.generate_key
into = args.passcode

saltyness = pass_deduction(into)

if generate_key:
    e.write_key()

encrypt_ = args.encrypt
decrypt_ = args.decrypt

if encrypt_ and decrypt_:
    raise TypeError("Please specify whether you want to encrypt the files or decrypt it.")
elif encrypt_:
    e.run(directory, saltyness, True)
elif decrypt_:
    e.run(directory, saltyness, False)
else:
    raise TypeError("Please specify whether you want to encrypt the files or decrypt it.")

