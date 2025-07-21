# app/auth.py
import sqlite3
from hashlib import sha256

# app/auth.py
def create_user_table():
    conn = sqlite3.connect('secure_file_storage.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Create files table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            file_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            owner_username TEXT NOT NULL,
            encryption_key TEXT NOT NULL,
            FOREIGN KEY (owner_username) REFERENCES users(username)
        )
    ''')
    
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect('secure_file_storage.db')
    cursor = conn.cursor()
    
    # Check if the username already exists
    cursor.execute('SELECT username FROM users WHERE username = ?', (username,))
    if cursor.fetchone():
        print("Username already exists. Please choose a different username.")
        conn.close()
        return False
    
    # If the username doesn't exist, register the user
    password_hash = sha256(password.encode()).hexdigest()
    cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
    conn.commit()
    conn.close()
    print("Registration successful!")
    return True

def authenticate_user(username, password):
    password_hash = sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('secure_file_storage.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] == password_hash if result else False