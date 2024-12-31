import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import ctypes
import sys

def create_password():
    subprocess.Popen(['python', 'tools/password.py'])

def show_password():
    subprocess.Popen(['python', 'tools/password-show-choose.py'])

def encode():
    subprocess.Popen(['python', 'tools/encode-file.py'])
root = tk.Tk()
root.resizable(False, False)
root.title("Server Application")
root.geometry("400x450")
root.config(bg="#2e3b4e")

style = {
    'bg': '#4e5b70',
    'fg': '#ffffff',
    'font': ('Helvetica', 12, 'bold'),
    'activebackground': '#627b8d',
    'width': 20
}

frame = tk.Frame(root, bg="#2e3b4e")

frame.pack(pady=40)

button_chat = tk.Button(frame, text="Create Password", command=create_password, **style)
button_chat.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

button_screen_sharing = tk.Button(frame, text="Show Passwords", command=show_password, **style)
button_screen_sharing.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

button_ftp = tk.Button(frame, text="Encode", command=encode, **style)
button_ftp.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
#
# button_decode = tk.Button(frame, text="Decode", command=start_decode, **style)
# button_decode.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
#
# button_user_connect = tk.Button(frame, text="User connect", command=start_user, **style)
# button_user_connect.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
#
# button_user_connect = tk.Button(frame, text="Create user", command=create_user, **style)
# button_user_connect.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
#
# # Расширение окна
# root.grid_columnconfigure(0, weight=1)
#
# label = tk.Label(root, text="Server Control Panel", font=('Helvetica', 16, 'bold'), fg='#ffffff', bg='#2e3b4e')
# label.pack(pady=10)
#
root.mainloop()
