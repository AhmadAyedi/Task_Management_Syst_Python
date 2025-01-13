import tkinter as tk
from tkinter import messagebox
import os

def sign_up():
    username = username_entry.get()
    password = password_entry.get()
    
    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    user_file = f"{username}.txt"
    if os.path.exists(user_file):
        messagebox.showerror("Error", "User already exists!")
        return

    with open(user_file, 'w') as file:
        file.write(f"{username}\n{password}\n")

    messagebox.showinfo("Success", "Account created successfully!")
    sign_up_win.destroy()
    login_window()

def login_user():
    username = username_entry.get()
    password = password_entry.get()
    
    user_file = f"{username}.txt"
    if not os.path.exists(user_file):
        messagebox.showerror("Error", "User does not exist!")
        return

    with open(user_file, 'r') as file:
        stored_username = file.readline().strip()
        stored_password = file.readline().strip()

    if username == stored_username and password == stored_password:
        messagebox.showinfo("Success", "Login successful!")
        login_win.destroy()
        open_task_manager(username)
    else:
        messagebox.showerror("Error", "Incorrect username or password!")

def add_task(username):
    task = task_entry.get()
    if task:
        with open(f"{username}.txt", 'a') as file:
            file.write(task + "\n")
        task_entry.delete(0, tk.END)
        load_tasks(username)

def load_tasks(username):
    task_listbox.delete(0, tk.END)
    with open(f"{username}.txt", 'r') as file:
        tasks = file.readlines()[2:]
    for task in tasks:
        task_listbox.insert(tk.END, task.strip())

def delete_task(username):
    selected_task = task_listbox.curselection()
    if selected_task:
        task_text = task_listbox.get(selected_task)
        task_listbox.delete(selected_task)

        with open(f"{username}.txt", 'r') as file:
            lines = file.readlines()
        with open(f"{username}.txt", 'w') as file:
            file.write(lines[0])
            file.write(lines[1])
            for line in lines[2:]:
                if line.strip() != task_text:
                    file.write(line)

def modify_task(username):
    selected_task = task_listbox.curselection()
    if selected_task:
        task_text = task_listbox.get(selected_task)
        task_listbox.delete(selected_task)
        task_entry.delete(0, tk.END)
        task_entry.insert(0, task_text)

        with open(f"{username}.txt", 'r') as file:
            lines = file.readlines()
        with open(f"{username}.txt", 'w') as file:
            file.write(lines[0])
            file.write(lines[1])
            for line in lines[2:]:
                if line.strip() != task_text:
                    file.write(line)

def open_task_manager(username):
    global task_entry, task_listbox

    task_win = tk.Toplevel(root)
    task_win.title(f"Task Manager - {username}")

    tk.Label(task_win, text="Task:").grid(row=0, column=0)
    task_entry = tk.Entry(task_win, width=40)
    task_entry.grid(row=0, column=1)

    tk.Button(task_win, text="Add Task", command=lambda: add_task(username), bg="#4CAF50", fg="white").grid(row=0, column=2)
    tk.Button(task_win, text="Delete Task", command=lambda: delete_task(username), bg="#F44336", fg="white").grid(row=1, column=2)
    tk.Button(task_win, text="Modify Task", command=lambda: modify_task(username), bg="#FFC107", fg="black").grid(row=2, column=2)

    task_listbox = tk.Listbox(task_win, width=50, height=15)
    task_listbox.grid(row=1, column=0, columnspan=2, rowspan=2)
    load_tasks(username)

    disconnect_button = tk.Button(task_win, text="Disconnect", command=lambda: [task_win.destroy(), main_window()], bg="#607D8B", fg="white")
    disconnect_button.grid(row=3, column=2, pady=10)

def sign_up_window():
    global username_entry, password_entry, sign_up_win

    sign_up_win = tk.Toplevel(root)
    sign_up_win.title("Sign Up")

    tk.Label(sign_up_win, text="Username:").grid(row=0, column=0)
    username_entry = tk.Entry(sign_up_win)
    username_entry.grid(row=0, column=1)

    tk.Label(sign_up_win, text="Password:").grid(row=1, column=0)
    password_entry = tk.Entry(sign_up_win, show="*")
    password_entry.grid(row=1, column=1)

    tk.Button(sign_up_win, text="Sign Up", command=sign_up, bg="#4CAF50", fg="white").grid(row=2, columnspan=2)

def login_window():
    global username_entry, password_entry, login_win

    login_win = tk.Toplevel(root)
    login_win.title("Login")

    tk.Label(login_win, text="Username:").grid(row=0, column=0)
    username_entry = tk.Entry(login_win)
    username_entry.grid(row=0, column=1)

    tk.Label(login_win, text="Password:").grid(row=1, column=0)
    password_entry = tk.Entry(login_win, show="*")
    password_entry.grid(row=1, column=1)

    tk.Button(login_win, text="Login", command=login_user, bg="#2196F3", fg="white").grid(row=2, columnspan=2)

def admin_interface():
    admin_win = tk.Toplevel(root)
    admin_win.title("Admin Interface")

    def refresh_users():
        user_listbox.delete(0, tk.END)
        for file in os.listdir():
            if file.endswith('.txt'):
                user_listbox.insert(tk.END, file.replace('.txt', ''))

    def delete_user():
        selected_user = user_listbox.curselection()
        if selected_user:
            username = user_listbox.get(selected_user)
            os.remove(f"{username}.txt")
            refresh_users()

    tk.Label(admin_win, text="User Accounts:").pack()
    user_listbox = tk.Listbox(admin_win)
    user_listbox.pack()
    refresh_users()

    tk.Button(admin_win, text="Delete User", command=delete_user, bg="#F44336", fg="white").pack(pady=5)

def main_window():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Welcome! Please choose an option:").pack(pady=10)
    tk.Button(root, text="Sign Up", command=sign_up_window, bg="#4CAF50", fg="white").pack(pady=5)
    tk.Button(root, text="Login", command=login_window, bg="#2196F3", fg="white").pack(pady=5)
    tk.Button(root, text="Admin", command=admin_interface, bg="#9C27B0", fg="white").pack(pady=5)

# Create the root window
root = tk.Tk()
root.title("Task Management System")
main_window()
root.mainloop()
