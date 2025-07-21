# app/file_manager.py
import sqlite3
from app.encryption import encrypt_file, decrypt_file
from app.utils import derive_key_from_password
import os

def upload_file(username, file_path):
    key = derive_key_from_password(username)
    encrypt_file(file_path, key)
    
    # Save the encrypted file in the common folder
    os.makedirs('storage/files', exist_ok=True)
    encrypted_file_path = f'storage/files/{os.path.basename(file_path)}.enc'
    os.rename(file_path + '.enc', encrypted_file_path)
    
    print(f"File saved at: {encrypted_file_path}")  # Debug print
    
    # Store file metadata in the database
    conn = sqlite3.connect('secure_file_storage.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO files (file_name, owner_username, encryption_key)
        VALUES (?, ?, ?)
    ''', (os.path.basename(file_path), username, key.hex()))
    conn.commit()
    conn.close()
    
    print(f"File '{file_path}' uploaded and encrypted.")
    

def share_file_key(owner_username, file_name, recipient_username):
    conn = sqlite3.connect('secure_file_storage.db')
    cursor = conn.cursor()
    
    # Get the encryption key for the file
    cursor.execute('''
        SELECT encryption_key FROM files
        WHERE file_name = ? AND owner_username = ?
    ''', (file_name, owner_username))
    result = cursor.fetchone()
    
    if result:
        key = bytes.fromhex(result[0])
        print(f"Share this key with '{recipient_username}':")
        print(f"Key: {key.hex()}")
    else:
        print("File not found or you do not own this file.")
    
    conn.close()

def download_file(username, file_name, key):
    # Ensure the file name does not include the .enc extension
    if file_name.endswith('.enc'):
        file_name = file_name[:-4]  # Remove the .enc extension
    
    encrypted_file_path = f'storage/files/{file_name}.enc'
    print(f"Looking for file at: {encrypted_file_path}")  # Debug print
    
    if os.path.exists(encrypted_file_path):
        # Verify the key
        conn = sqlite3.connect('secure_file_storage.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT encryption_key FROM files
            WHERE file_name = ? AND owner_username = ?
        ''', (file_name, username))
        result = cursor.fetchone()
        conn.close()
        
        if result and bytes.fromhex(result[0]) == key:
            decrypt_file(encrypted_file_path, key)
            print(f"File '{file_name}' downloaded and decrypted.")
        else:
            print("Invalid key. You do not have permission to download this file.")
    else:
        print(f"File '{file_name}' not found.")