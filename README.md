# To-Do-Planner-GUI-Software-
This project is a simple To-Do List application built using Python's tkinter for the graphical user interface (GUI) and sqlite3 for managing the task and user data in a database. Below are the descriptions and functions of the major components in the project:

Descriptions and Functions:
Database Setup (setup_db)

Function: Initializes the database by creating two tables: users (for user authentication) and tasks (for storing to-do tasks). If the tables already exist, it does nothing.
Details:
The users table contains columns: id, username, and password.
The tasks table contains columns: id, task_name, due_date, priority, status, category, recurring, and user_id.
The user_id field in the tasks table links each task to a user.
User Registration (register_user)

Function: Registers a new user by inserting the username and password into the users table. If the username is already taken, it shows a warning.
Details: Uses sqlite3 to insert a new record into the database.
User Login (login)

Function: Validates the user's credentials by checking if the entered username and password match a record in the users table. On successful login, the user’s ID is stored in current_user_id, and the To-Do List window opens.
Details: The function fetches user data from the users table and compares it with the entered username and password.
Opening To-Do List Window (open_todo_list)

Function: Opens the To-Do List window where users can manage their tasks. It allows users to add, edit, delete, and mark tasks as completed.
Details: The window contains:
Input fields for task name, due date, priority, category, and recurrence.
A Treeview widget to display tasks.
Buttons for adding, editing, deleting, and marking tasks as completed.
Add Task (add_task)

Function: Adds a new task to the database based on user input and refreshes the task list.
Details: After adding the task to the tasks table, it refreshes the task list view and clears the input fields.
Load Tasks (load_tasks)

Function: Loads and displays the tasks for the currently logged-in user in the Treeview widget.
Details: Fetches tasks from the database and inserts them into the Treeview. Only tasks belonging to the logged-in user (current_user_id) are displayed.
Delete Task (delete_task)

Function: Deletes a selected task from the database.
Details: When a task is selected, its id is retrieved, and it is removed from the database. The task list is then refreshed.
Edit Task (edit_task)

Function: Allows the user to edit the details of a selected task.
Details: The task's details (name, due date, priority, category, and recurrence) are retrieved, and the user is prompted to update them. After updating, the task is saved back into the database, and the task list is refreshed.
Mark Task as Completed (mark_completed)

Function: Changes the status of a selected task to "Completed."
Details: Updates the status field of the task in the database and refreshes the task list to reflect the change.
Clear Input Fields (clear_fields)

Function: Clears the input fields for task name, due date, priority, category, and recurrence after adding or editing a task.
Details: Ensures that the fields are empty after each operation.
Main Login Window

Function: Provides a login interface where users can enter their username and password or register as a new user.
Details:
Contains fields for entering a username and password.
Provides options to log in or register a new user.
If the user logs in successfully, the To-Do List window opens.
Task Categories and Recurrence

Categories: Tasks can be categorized as "Work", "Personal", "Shopping", or "Other".
Recurrence: Tasks can be marked as recurring ("Yes" or "No"), though handling for recurring tasks is not implemented in this code.
Summary of How the System Works:
The user logs in with their username and password, or registers a new account.
Upon successful login, the main To-Do List interface opens where the user can:
Add new tasks with details like task name, due date, priority, category, and recurrence.
Edit or delete existing tasks.
Mark tasks as "Completed."
All tasks are saved in a SQLite database, associated with the logged-in user via the user_id.
Technologies Used:
tkinter: For building the GUI (graphical user interface).
sqlite3: For database management (storing users and tasks).
simpledialog: For input dialogs that allow users to edit task details.
