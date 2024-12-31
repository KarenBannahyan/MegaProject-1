import socket
import mysql.connector
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading

# Функция для подключения к базе данных MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  # Адрес базы данных
        user="root",  # Имя пользователя MySQL
        password="Karen1234",  # Пароль пользователя MySQL
        database="base"  # Имя базы данных
    )


# Функция для получения пароля из базы данных по имени пользователя
def get_password_from_db(username):
    try:
        conn = get_db_connection()  # Получаем подключение к базе данных
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM user_passwords WHERE name=%s", (username,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None


# Функция для проверки правильности ключа
def check_key_from_client(stored_password, key_from_client):
    stored_password = stored_password.strip()
    key_from_client = key_from_client.strip()

    print(f"Comparing stored password: '{stored_password}' with client key: '{key_from_client}'")

    if stored_password == key_from_client:
        return True
    return False


# Серверная логика для обработки запроса от клиента
def handle_client(connection, address, text_widget):
    try:
        text_widget.insert(tk.END, f"Connection from {address}\n")
        data = connection.recv(1024).decode('utf-8')  # Используем UTF-8 кодировку
        text_widget.insert(tk.END, f"Received data from client: {data}\n")

        if data:
            username, key_from_client = data.split(":")
            text_widget.insert(tk.END, f"Username: {username}, Key: {key_from_client}\n")

            # Получаем пароль для пользователя из базы данных
            stored_password = get_password_from_db(username)

            if stored_password:
                if check_key_from_client(stored_password, key_from_client):
                    response = "Key is correct"
                else:
                    response = "Invalid key"
            else:
                response = f"Username '{username}' not found!"

            text_widget.insert(tk.END, f"Response: {response}\n")
            connection.send(response.encode('utf-8'))  # Отправляем ответ клиенту
    except Exception as e:
        text_widget.insert(tk.END, f"Error handling client: {e}\n")
    finally:
        connection.close()


# Настройка сервера
def start_server(host, port, text_widget):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    text_widget.insert(tk.END, f"Server listening on {host}:{port}\n")

    while True:
        try:
            connection, address = server_socket.accept()
            threading.Thread(target=handle_client, args=(connection, address, text_widget), daemon=True).start()
        except KeyboardInterrupt:
            text_widget.insert(tk.END, "Server has been interrupted. Shutting down...\n")
            break  # Закрыть сервер в случае прерывания
        except Exception as e:
            text_widget.insert(tk.END, f"Error accepting connection: {e}\n")

    server_socket.close()


# GUI интерфейс для сервера
def start_gui():
    style = {
        'bg': '#4e5b70',
        'fg': '#ffffff',
        'font': ('Helvetica', 12, 'bold'),
        'activebackground': '#627b8d',
        'width': 20,
        'height': 2
    }

    root = tk.Tk()
    root.title("Server")
    root.geometry("600x570")
    root.config(bg='#4e5b70')  # Цвет фона окна

    # Title label
    title_label = tk.Label(root, text="Server Authentication", **style)
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

    # Text box to display server logs
    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=('Helvetica', 10), width=70, height=15)
    text_widget.pack(pady=10)
    text_widget.config(state=tk.DISABLED)  # Отключаем редактирование

    # Start server button
    def start_server_button():
        host = entry_ip.get()
        try:
            port = int(entry_port.get())  # Преобразуем в число
            text_widget.config(state=tk.NORMAL)  # Включаем редактирование текстового поля
            threading.Thread(target=start_server, args=(host, port, text_widget), daemon=True).start()  # Запуск сервера в отдельном потоке
        except ValueError:
            messagebox.showerror("Error", "Invalid port number!")

    start_button = tk.Button(root, text="Start Server", command=start_server_button, **style)
    start_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    start_gui()
