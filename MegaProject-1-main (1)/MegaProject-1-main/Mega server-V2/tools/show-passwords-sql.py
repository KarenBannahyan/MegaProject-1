import tkinter as tk
from tkinter import messagebox
import mysql.connector


# Function to load content from MySQL
def load_from_mysql():
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",  # Database address
            user="root",  # MySQL username
            password="Karen1234",  # MySQL password
            database="base"  # Database name
        )

        cursor = conn.cursor()

        # SQL query to select all passwords from the table
        cursor.execute("SELECT goal, password FROM passwords")
        rows = cursor.fetchall()

        if not rows:
            messagebox.showinfo("Info", "No records found in the database.")
            return

        # Display the data in the text widget
        text_area.delete(1.0, tk.END)  # Clear any previous content
        for row in rows:
            goal, password = row
            text_area.insert(tk.END, f"Goal: {goal} | Password: {password}\n")

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error reading from MySQL: {err}")


# Create the main window
root = tk.Tk()
root.title("Passwords from MySQL")

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

# Create a button to load passwords from MySQL
load_button = tk.Button(root, text="Load Passwords from MySQL", command=load_from_mysql, **style)
load_button.pack(pady=20)

# Create a text area to display the data from MySQL
text_area = tk.Text(root, width=50, height=15, font=('Helvetica', 12), wrap=tk.WORD)
text_area.pack(pady=10)

# Run the application
root.mainloop()
