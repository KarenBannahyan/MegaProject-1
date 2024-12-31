import tkinter as tk
from tkinter import messagebox
import mysql.connector
from cryptography.fernet import Fernet
import subprocess  # For server.py and client.py

style = {
    'bg': '#4e5b70',
    'fg': '#ffffff',
    'font': ('Helvetica', 12, 'bold'),
    'activebackground': '#627b8d',
    'width': 20
}

def local():
    subprocess.Popen(['python', 'tools/show-passwords.py'])

def sql():
    subprocess.Popen(['python', 'tools/show-passwords-sql.py'])
root = tk.Tk()
root.resizable(False, False)
root.title("Programm with server and client")
root.geometry("400x250")
root.config(bg='#4e5b70')

server_button = tk.Button(root, text="Local(Txt)", command=local, **style)
client_button = tk.Button(root, text="MySql", command=sql, **style)

server_button.place(relx=0.5, rely=0.3, anchor="center")
client_button.place(relx=0.5, rely=0.6, anchor="center")

root.mainloop()
