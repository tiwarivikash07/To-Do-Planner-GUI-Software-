import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
from datetime import datetime, timedelta

# Database setup for tasks and users
def setup_db():
    conn = sqlite3.connect('todo_list.db')
    c = conn.cursor()
    
    # Create user table for authentication
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT)''')

    # Create tasks table
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_name TEXT,
                    due_date TEXT,
                    priority TEXT,
                    status TEXT,
                    category TEXT,
                    recurring TEXT,
                    user_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

# Register a new user
def register_user(username, password):
    conn = sqlite3.connect('todo_list.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showwarning("Username Taken", "This username is already taken.")
    finally:
        conn.close()

# Check user credentials
def check_credentials(username, password):
    conn = sqlite3.connect('todo_list.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

# Function to handle user login
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    if username and password:
        user = check_credentials(username, password)
        if user:
            global current_user_id
            current_user_id = user[0]  # Store the current logged-in user's ID
            login_window.destroy()  # Close the login window
            open_todo_list()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    else:
        messagebox.showwarning("Input Error", "Please enter both username and password.")

# Function to handle user registration
def register():
    username = username_entry.get()
    password = password_entry.get()
    
    if username and password:
        register_user(username, password)
        messagebox.showinfo("Registration Success", "User registered successfully. Please login.")
    else:
        messagebox.showwarning("Input Error", "Please enter both username and password.")

# Function to open the To-Do List window after successful login
def open_todo_list():
    todo_list_window = tk.Tk()
    todo_list_window.title("To-Do List")

    # Task Name Entry
    task_name_label = tk.Label(todo_list_window, text="Task Name:")
    task_name_label.grid(row=0, column=0, padx=10, pady=10)
    task_name_entry = tk.Entry(todo_list_window, width=40)
    task_name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Due Date Entry
    due_date_label = tk.Label(todo_list_window, text="Due Date (YYYY-MM-DD):")
    due_date_label.grid(row=1, column=0, padx=10, pady=10)
    due_date_entry = tk.Entry(todo_list_window, width=40)
    due_date_entry.grid(row=1, column=1, padx=10, pady=10)

    # Priority Combobox
    priority_label = tk.Label(todo_list_window, text="Priority:")
    priority_label.grid(row=2, column=0, padx=10, pady=10)
    priority_combobox = ttk.Combobox(todo_list_window, values=["High", "Medium", "Low"], width=37)
    priority_combobox.grid(row=2, column=1, padx=10, pady=10)

    # Category Combobox
    category_label = tk.Label(todo_list_window, text="Category:")
    category_label.grid(row=3, column=0, padx=10, pady=10)
    category_combobox = ttk.Combobox(todo_list_window, values=["Work", "Personal", "Shopping", "Other"], width=37)
    category_combobox.grid(row=3, column=1, padx=10, pady=10)

    # Recurring Combobox
    recurring_label = tk.Label(todo_list_window, text="Recurring (Yes/No):")
    recurring_label.grid(row=4, column=0, padx=10, pady=10)
    recurring_combobox = ttk.Combobox(todo_list_window, values=["Yes", "No"], width=37)
    recurring_combobox.grid(row=4, column=1, padx=10, pady=10)

    # Add Task Button
    add_task_button = tk.Button(todo_list_window, text="Add Task", width=20, command=lambda: add_task(todo_list_window, task_name_entry, due_date_entry, priority_combobox, category_combobox, recurring_combobox))
    add_task_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # Task List (Treeview)
    task_list_tree = ttk.Treeview(todo_list_window, columns=("Task", "Due Date", "Priority", "Status", "Category", "Recurring"), show="headings")
    task_list_tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    task_list_tree.heading("Task", text="Task")
    task_list_tree.heading("Due Date", text="Due Date")
    task_list_tree.heading("Priority", text="Priority")
    task_list_tree.heading("Status", text="Status")
    task_list_tree.heading("Category", text="Category")
    task_list_tree.heading("Recurring", text="Recurring")

    # Buttons for actions
    delete_button = tk.Button(todo_list_window, text="Delete Task", width=20, command=lambda: delete_task(todo_list_window, task_list_tree))
    delete_button.grid(row=7, column=0, padx=10, pady=10)

    edit_button = tk.Button(todo_list_window, text="Edit Task", width=20, command=lambda: edit_task(todo_list_window, task_list_tree))
    edit_button.grid(row=7, column=1, padx=10, pady=10)

    complete_button = tk.Button(todo_list_window, text="Mark Completed", width=20, command=lambda: mark_completed(todo_list_window, task_list_tree))
    complete_button.grid(row=8, column=0, padx=10, pady=10)

    # Load existing tasks
    load_tasks(todo_list_window, task_list_tree)

    todo_list_window.mainloop()

# Add task to database
def add_task(window, task_name_entry, due_date_entry, priority_combobox, category_combobox, recurring_combobox):
    task_name = task_name_entry.get()
    due_date = due_date_entry.get()
    priority = priority_combobox.get()
    category = category_combobox.get()
    recurring = recurring_combobox.get()

    if not task_name:
        messagebox.showwarning("Input Error", "Task name cannot be empty!")
        return

    conn = sqlite3.connect('todo_list.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task_name, due_date, priority, status, category, recurring, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (task_name, due_date, priority, 'Pending', category, recurring, current_user_id))
    conn.commit()
    conn.close()

    load_tasks(window, task_list_tree)
    clear_fields(task_name_entry, due_date_entry, priority_combobox, category_combobox, recurring_combobox)

# Load tasks from the database and display them
def load_tasks(window, treeview):
    for row in treeview.get_children():
        treeview.delete(row)

    conn = sqlite3.connect('todo_list.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE user_id=?", (current_user_id,))
    tasks = c.fetchall()

    for task in tasks:
        treeview.insert('', 'end', values=task[1:])
    conn.close()

# Delete a selected task
def delete_task(window, treeview):
    selected_item = treeview.selection()
    if selected_item:
        task_id = treeview.item(selected_item, 'values')[0]
        conn = sqlite3.connect('todo_list.db')
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
        load_tasks(window, treeview)

# Edit task information
def edit_task(window, treeview):
    selected_item = treeview.selection()
    if selected_item:
        task_data = treeview.item(selected_item, 'values')
        task_id = task_data[0]
        
        new_task_name = simpledialog.askstring("Edit Task", "Enter new task name:", initialvalue=task_data[1])
        if not new_task_name:
            return

        new_due_date = simpledialog.askstring("Edit Task", "Enter new due date (YYYY-MM-DD):", initialvalue=task_data[2])
        new_priority = simpledialog.askstring("Edit Task", "Enter new priority:", initialvalue=task_data[3])
        new_category = simpledialog.askstring("Edit Task", "Enter new category:", initialvalue=task_data[4])
        new_recurring = simpledialog.askstring("Edit Task", "Enter new recurring (Yes/No):", initialvalue=task_data[5])

        conn = sqlite3.connect('todo_list.db')
        c = conn.cursor()
        c.execute("UPDATE tasks SET task_name=?, due_date=?, priority=?, category=?, recurring=? WHERE id=?",
                  (new_task_name, new_due_date, new_priority, new_category, new_recurring, task_id))
        conn.commit()
        conn.close()

        load_tasks(window, treeview)

# Mark task as completed
def mark_completed(window, treeview):
    selected_item = treeview.selection()
    if selected_item:
        task_id = treeview.item(selected_item, 'values')[0]
        conn = sqlite3.connect('todo_list.db')
        c = conn.cursor()
        c.execute("UPDATE tasks SET status=? WHERE id=?", ('Completed', task_id))
        conn.commit()
        conn.close()
        load_tasks(window, treeview)

# Clear the entry fields after adding/editing a task
def clear_fields(task_name_entry, due_date_entry, priority_combobox, category_combobox, recurring_combobox):
    task_name_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)
    priority_combobox.set('')
    category_combobox.set('')
    recurring_combobox.set('')

# Setup initial database
setup_db()

# Main Login Window
login_window = tk.Tk()
login_window.title("Login")

# Username Entry
username_label = tk.Label(login_window, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(login_window, width=30)
username_entry.grid(row=0, column=1, padx=10, pady=10)

# Password Entry
password_label = tk.Label(login_window, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(login_window, show="*", width=30)
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Login Button
login_button = tk.Button(login_window, text="Login", width=20, command=login)
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Register Button
register_button = tk.Button(login_window, text="Register", width=20, command=register)
register_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Start the login window loop
login_window.mainloop()
