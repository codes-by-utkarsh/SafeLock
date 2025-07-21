# app/database.py
import sqlite3

def create_user_table():
    conn = sqlite3.connect('secure_file_storage.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()