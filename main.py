# main.py
from app.auth import authenticate_user, register_user, create_user_table
from app.file_manager import upload_file, download_file, share_file_key

def main():
    create_user_table()  # Initialize the database

    print("Welcome to Secure File Storage!")
    action = input("Do you want to (1) Register or (2) Login? ")

    if action == "1":
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        if register_user(username, password):
            print("Registration successful!")
        else:
            print("Registration failed. Please try again.")
    elif action == "2":
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if authenticate_user(username, password):
            print("Login successful!")
            while True:
                print("\nWhat would you like to do?")
                print("1. Upload a file")
                print("2. Download a file")
                print("3. Share a file key")
                print("4. Exit")
                choice = input("Enter your choice: ")

                if choice == "1":
                    file_path = input("Enter the file path to upload: ")
                    upload_file(username, file_path)
                elif choice == "2":
                    file_name = input("Enter the file name to download: ")
                    key_hex = input("Enter the encryption key (in hex): ")
                    key = bytes.fromhex(key_hex)
                    download_file(username, file_name, key)
                elif choice == "3":
                    file_name = input("Enter the file name to share: ")
                    recipient_username = input("Enter the recipient's username: ")
                    share_file_key(username, file_name, recipient_username)
                elif choice == "4":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Try again.")
        else:
            print("Invalid username or password.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()