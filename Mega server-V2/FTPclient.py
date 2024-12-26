import socket
from tkinter import Tk, filedialog, messagebox, Entry, Label, Button
from PIL import Image
from io import BytesIO

# Стиль для кнопок и текстовых полей
style = {
    'bg': '#4e5b70',
    'fg': '#ffffff',
    'font': ('Helvetica', 12, 'bold'),
    'width': 20
}


def send_image(image_path, host, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        filename = image_path.split('/')[-1]
        filename_length = len(filename).to_bytes(4, byteorder='big')
        client_socket.send(filename_length)
        client_socket.send(filename.encode())

        with open(image_path, 'rb') as f:
            image_data = f.read()

        file_size = len(image_data).to_bytes(8, byteorder='big')
        client_socket.send(file_size)

        client_socket.send(image_data)

        print(f"Photo {filename} was send to server.")
        messagebox.showinfo("Success", f"Photo {filename} was successfully send!")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Cant send photo: {e}")
    finally:
        client_socket.close()


def select_image(host, port):
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Choose photo",
                                           filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if file_path:
        send_image(file_path, host, port)


def create_gui():
    root = Tk()
    root.title("FTP Photo client")
    root.resizable(False, False)

    ip_label = Label(root, text="Servers IP address:", **style)
    ip_label.grid(row=0, column=0, padx=10, pady=5)

    ip_entry = Entry(root, **style)
    ip_entry.grid(row=0, column=1, padx=10, pady=5)
    ip_entry.insert(0, "127.0.0.1")

    port_label = Label(root, text="Servers Port:", **style)
    port_label.grid(row=1, column=0, padx=10, pady=5)

    port_entry = Entry(root, **style)
    port_entry.grid(row=1, column=1, padx=10, pady=5)
    port_entry.insert(0, "65432")

    send_button = Button(root, text="Choose photo", **style,
                         command=lambda: select_image(ip_entry.get(), int(port_entry.get())))
    send_button.grid(row=2, columnspan=2, padx=10, pady=20)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
