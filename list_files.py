import sqlite3

def list_files():
    conn = sqlite3.connect('secure_file_storage.db')
    cursor = conn.cursor()
    cursor.execute('SELECT file_name, owner_username FROM files')
    files = cursor.fetchall()
    conn.close()
    
    if files:
        print("Files in the database:")
        for file in files:
            print(f"File: {file[0]}, Owner: {file[1]}")
    else:
        print("No files found in the database.")

# Call the function to list files
list_files()