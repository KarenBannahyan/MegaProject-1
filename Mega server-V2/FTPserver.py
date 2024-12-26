import socket
import os
import threading
from tkinter import Tk, Button, Label, Entry
from PIL import Image, ImageTk
from io import BytesIO

if not os.path.exists('photos'):
    os.makedirs('photos')

# Стиль для кнопок
style = {
    'bg': '#4e5b70',
    'fg': '#ffffff',
    'font': ('Helvetica', 12, 'bold'),
    'activebackground': '#627b8d',
    'width': 20
}

class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FTP Photo Server")
        self.root.geometry("600x600")
        self.root.configure(bg=style['bg'])

        self.header_label = Label(self.root, text="Server Settings", fg=style['fg'], bg=style['bg'], font=('Helvetica', 16, 'bold'))
        self.header_label.pack(pady=10)

        self.ip_label = Label(self.root, text="IP Address:", fg=style['fg'], bg=style['bg'])
        self.ip_label.pack(pady=5)
        self.ip_entry = Entry(self.root, font=('Helvetica', 12), width=20)
        self.ip_entry.insert(0, '127.0.0.1')
        self.ip_entry.pack(pady=5)

        self.port_label = Label(self.root, text="Port:", fg=style['fg'], bg=style['bg'])
        self.port_label.pack(pady=5)
        self.port_entry = Entry(self.root, font=('Helvetica', 12), width=20)
        self.port_entry.insert(0, '65432')
        self.port_entry.pack(pady=5)

        self.start_button = Button(self.root, text="Turn on server", command=self.start_server, **style)
        self.start_button.pack(pady=20)

        self.image_label = Label(self.root, bg=style['bg'])
        self.image_label.pack(pady=20)

    def start_server(self):
        ip_address = self.ip_entry.get()
        try:
            port = int(self.port_entry.get())
        except ValueError:
            print("Error: Invalid Port.")
            return

        self.start_button.config(state="disabled")


        server_thread = threading.Thread(target=start_server, args=(self, ip_address, port))
        server_thread.daemon = True
        server_thread.start()

    def display_image(self, image_path):
        img = Image.open(image_path)
        img.thumbnail((400, 400))
        img_tk = ImageTk.PhotoImage(img)

        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

def handle_client(client_socket, app):
    try:
        filename_length = client_socket.recv(4)
        if not filename_length:
            return

        filename_length = int.from_bytes(filename_length, byteorder='big')
        filename = client_socket.recv(filename_length).decode()

        file_size = client_socket.recv(8)
        file_size = int.from_bytes(file_size, byteorder='big')

        image_data = b""
        while len(image_data) < file_size:
            image_data += client_socket.recv(4096)

        image_path = os.path.join('photos', filename)
        with open(image_path, 'wb') as f:
            f.write(image_data)
        print(f"File {filename} saved.")

        app.display_image(image_path)
    finally:
        client_socket.close()

def start_server(app, ip_address, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port))
    server_socket.listen(5)
    print(f"Server is on {ip_address}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        handle_client(client_socket, app)

if __name__ == "__main__":
    root = Tk()
    app = ServerApp(root)
    root.mainloop()
