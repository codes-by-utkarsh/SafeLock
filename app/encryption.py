# app/encryption.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    with open(file_path + '.enc', 'wb') as f:
        f.write(iv + encrypted_data)

def decrypt_file(encrypted_file_path, key):
    with open(encrypted_file_path, 'rb') as f:
        iv = f.read(16)
        encrypted_data = f.read()
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    with open(encrypted_file_path[:-4], 'wb') as f:
        f.write(decrypted_data)