import tkinter as tk
from tkinter import messagebox
import random
import string
import hashlib
import pyperclip
import mysql.connector
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
from base64 import b64encode, b64decode

# Function to generate a password
def generate_password(keyword):
    password_length = 16
    all_characters = string.ascii_letters + string.digits + "!@#$&*()"
    random_part = ''.join(random.choice(all_characters) for i in range(password_length - len(keyword)))
    password = keyword + random_part
    password = ''.join(random.sample(password, len(password)))
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return password, hashed_password


# Function to check if the table exists, and if not, create it
def create_mysql_table():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Database address
            user="root",  # MySQL username
            password="Karen1234",  # MySQL password
            database="base"  # Database name
        )
        cursor = conn.cursor()

        # SQL query to create the table if it doesn't exist
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS passwords (
            id INT AUTO_INCREMENT PRIMARY KEY,
            goal VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        '''
        cursor.execute(create_table_query)
        conn.commit()

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error creating table in MySQL: {err}")


# Function to save password to MySQL
def save_to_mysql(goal, password):
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Database address
            user="root",  # MySQL username
            password="Karen1234",  # MySQL password
            database="base"  # Database name
        )
        cursor = conn.cursor()

        # SQL query to insert password
        query = "INSERT INTO passwords (goal, password) VALUES (%s, %s)"
        cursor.execute(query, (goal, password))
        conn.commit()

        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Password saved to MySQL!")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error saving to MySQL: {err}")


# Function to save password to file
def save_to_file(goal, password):
    try:
        # Get the current working directory
        file_path = os.path.join(os.getcwd(), "passwords.txt")

        # Write goal and password to the file
        with open(file_path, "a") as f:
            f.write(f"Goal: {goal} | Password: {password}\n")

        messagebox.showinfo("Success", f"Password saved to {file_path}!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save to file: {e}")


# Function to handle password generation on button click
def on_generate_click():
    keyword = keyword_entry.get()
    goal = goal_entry.get()
    mysql_choice = mysql_choice_entry.get().strip().lower()
    file_choice = file_choice_entry.get().strip().lower()

    if not keyword:
        messagebox.showerror("Error", "Please enter a keyword for password generation!")
        return

    if not goal:
        messagebox.showerror("Error", "Please enter the password goal!")
        return

    password, hashed_password = generate_password(keyword)
    result_label.config(text=f"Generated Password:\n{password}\n\n(Hashed Password: {hashed_password})")

    # Create the MySQL table if it doesn't exist
    create_mysql_table()

    # Save to MySQL if the user chose 'Yes'
    if mysql_choice == 'yes':
        save_to_mysql(goal, password)

    # Save to file if the user chose 'Yes'
    if file_choice == 'yes':
        save_to_file(goal, password)

    if mysql_choice != 'yes' and file_choice != 'yes':
        messagebox.showwarning("Warning", "Password not saved anywhere. Choose at least one save option.")

    global current_password
    current_password = password


# Function to copy password to clipboard
def copy_to_clipboard():
    try:
        pyperclip.copy(current_password)
        messagebox.showinfo("Success", "Password copied to clipboard!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy password: {str(e)}")


# Create the main window
root = tk.Tk()
root.title("Password Generator")

# Style for UI elements
style = {
    'bg': '#4e5b70',
    'fg': '#ffffff',
    'font': ('Helvetica', 12, 'bold'),
    'activebackground': '#627b8d',
    'width': 20
}

# Configure window
root.geometry("500x500")
root.config(bg="#3e4b59")
root.resizable(False, False)

# Create widgets with the defined style
keyword_label = tk.Label(root, text="Enter Keyword:", **style)
keyword_label.pack(pady=10)

keyword_entry = tk.Entry(root, width=30, font=('Helvetica', 12), bd=2, relief="solid")
keyword_entry.pack(pady=10)

goal_label = tk.Label(root, text="Enter Goal of Password:", **style)
goal_label.pack(pady=10)

goal_entry = tk.Entry(root, width=30, font=('Helvetica', 12), bd=2, relief="solid")
goal_entry.pack(pady=10)

mysql_label = tk.Label(root, text="Save to MySQL? (Yes/No):", **style)
mysql_label.pack(pady=5)

mysql_choice_entry = tk.Entry(root, width=30, font=('Helvetica', 12), bd=2, relief="solid")
mysql_choice_entry.pack(pady=5)

file_label = tk.Label(root, text="Save to File? (Yes/No):", **style)
file_label.pack(pady=5)

file_choice_entry = tk.Entry(root, width=30, font=('Helvetica', 12), bd=2, relief="solid")
file_choice_entry.pack(pady=5)

generate_button = tk.Button(root, text="Generate Password", command=on_generate_click, **style)
generate_button.pack(pady=10)

copy_button = tk.Button(root, text="Copy Password", command=copy_to_clipboard, **style)
copy_button.pack(pady=10)

result_label = tk.Label(root, text="", justify=tk.LEFT, **style)
result_label.pack(pady=15)

# Global variable to store the password
current_password = ""

# Run the application
root.mainloop()
