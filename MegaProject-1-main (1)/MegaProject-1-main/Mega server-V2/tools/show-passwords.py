import tkinter as tk
from tkinter import messagebox
import os


# Function to load content of passwords.txt
def load_passwords():
    try:
        file_path = os.path.join(os.getcwd(), "passwords.txt")

        if not os.path.exists(file_path):
            messagebox.showerror("Error", "passwords.txt file not found!")
            return

        with open(file_path, "r") as file:
            content = file.readlines()

        if not content:
            messagebox.showinfo("Info", "The file is empty.")
            return

        # Display the content in the text widget
        text_area.delete(1.0, tk.END)  # Clear any previous content
        text_area.insert(tk.END, "".join(content))  # Insert new content
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")


# Create the main window
root = tk.Tk()
root.title("Passwords File Viewer")

# Style for UI elements
style = {
    'bg': '#4e5b70',
    'fg': '#ffffff',
    'font': ('Helvetica', 12, 'bold'),
    'activebackground': '#627b8d',
    'width': 20
}

# Configure window
root.geometry("500x400")
root.config(bg="#3e4b59")

# Create a button to load passwords from file
load_button = tk.Button(root, text="Load Passwords", command=load_passwords, **style)
load_button.pack(pady=20)

# Create a text area to display the file content
text_area = tk.Text(root, width=50, height=15, font=('Helvetica', 12), wrap=tk.WORD)
text_area.pack(pady=10)

# Run the application
root.mainloop()
