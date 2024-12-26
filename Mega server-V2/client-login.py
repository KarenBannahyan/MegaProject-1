import socket
import tkinter as tk
from tkinter import messagebox
import subprocess

def send_key_to_server(host, port, username, key_str):
    try:
        # Соединение с сервером
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            message = f"{username}:{key_str}"
            s.sendall(message.encode())  # Обратите внимание на кодировку

            # Получаем ответ от сервера
            response = s.recv(1024).decode('utf-8')  # Обратите внимание на кодировку
            return response
    except Exception as e:
        messagebox.showerror("Error", f"Connection error: {e}")
        return None


# Функция проверки ключа, вызывающая сервер
def check_client_key(username, key_str, host, port):
    if not key_str:
        messagebox.showerror("Error", "Key not found!")
        return

    try:
        response = send_key_to_server(host, port, username, key_str)
        if response:
            if response == "Key is correct":
                messagebox.showinfo("Success", "Key is correct!")
                subprocess.Popen(['python', 'main-client.py'])
                # Дальнейшие действия, например запуск приложения
            else:
                messagebox.showerror("Error", response)
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")


# Пример интерфейса для ввода имени пользователя и ключа
def start_client():
    style = {
        'bg': '#4e5b70',
        'fg': '#ffffff',
        'font': ('Helvetica', 12, 'bold'),
        'activebackground': '#627b8d',
        'width': 20,
        'height': 2
    }

    root = tk.Tk()
    root.resizable(False, False)
    root.title("Client")
    root.geometry("500x500")
    root.config(bg='#4e5b70')  # Цвет фона окна

    # Title label
    title_label = tk.Label(root, text="Client Authentication", **style)
    title_label.config(font=('Helvetica', 16, 'bold'))
    title_label.pack(pady=20)

    # IP Address label and entry
    ip_label = tk.Label(root, text="Server IP Address:", bg='#4e5b70', fg='#ffffff', font=('Helvetica', 12))
    ip_label.pack(pady=5)
    entry_ip = tk.Entry(root, font=('Helvetica', 12), width=25)
    entry_ip.pack(pady=5)
    entry_ip.insert(0, '127.0.0.1')  # Значение по умолчанию

    # Port label and entry
    port_label = tk.Label(root, text="Server Port:", bg='#4e5b70', fg='#ffffff', font=('Helvetica', 12))
    port_label.pack(pady=5)
    entry_port = tk.Entry(root, font=('Helvetica', 12), width=25)
    entry_port.pack(pady=5)
    entry_port.insert(0, '65432')  # Значение по умолчанию

    # Username label and entry
    username_label = tk.Label(root, text="Username:", bg='#4e5b70', fg='#ffffff', font=('Helvetica', 12))
    username_label.pack(pady=5)
    entry_username = tk.Entry(root, font=('Helvetica', 12), width=25)
    entry_username.pack(pady=5)

    # Key label and entry
    key_label = tk.Label(root, text="Password:", bg='#4e5b70', fg='#ffffff', font=('Helvetica', 12))
    key_label.pack(pady=5)
    entry_key = tk.Entry(root, font=('Helvetica', 12), show="*", width=25)
    entry_key.pack(pady=5)

    # Submit button
    submit_button = tk.Button(root, text="Submit", command=lambda: on_submit(entry_username, entry_key, entry_ip, entry_port), **style)
    submit_button.pack(pady=20)

    # Function to handle the submit action
    def on_submit(entry_username, entry_key, entry_ip, entry_port):
        username = entry_username.get()
        key_str = entry_key.get()
        host = entry_ip.get()
        try:
            port = int(entry_port.get())  # Преобразуем в число
            check_client_key(username, key_str, host, port)
        except ValueError:
            messagebox.showerror("Error", "Invalid port number!")

    root.mainloop()


if __name__ == "__main__":
    start_client()
