# TO DO OR NOT TO DO
#### Video Demo: 
#### Description:
To Do or Not To Do is a simple To-Do List web app made using html, css, and python (flask).

The **app.py** file is the python file that contains all of my flask code. The main functions in the file are @login_required, register(), login(), shakespeare(), newtask(), index(), completed(), and logout()

The **information.db** file contains that SQL database needed for the web app. In it are two tables. One of them is called "users", and tracks users' login info (username, user_id, and a hash of their password). The second table is called "tasks", and tracks task information (task_id, user_id, task_string, whether the task is completed or not (boolean value), when the task was created and when the task was completed (if it was)).

The **commands.sql** file contains two SQL commands, in case the database needed to be resetted.

In the templates folder, there are seven html files.

**layout.html** contains the basic layout for all of the html templates. It has a navigation bar that displays different navigation options depending on whether the user is logged in or not. If the user is not logged in, it will display 'Login' and 'Register'. If the user *is* logged in, it will display 'Add a New Task', 'Completed Tasks', and 'Logout'. Whether the user is logged in or not, the navbar will also display a picture of shakespeare (that can be clicked on and directs user to a separate page) as well as the name of the project, 'To Do or Not To Do' (directs the user to the homepage).

**login.html** shows a page where the user can input a username and password to log into their account. It will show a warning if user doesn't input proper information (not inputting a username/password, inputting the wrong password, etc.). This page automatically shows when web app is launched and if user tries to go to homepage.

**register.html** shows a page where the user can input a username, password, and confirmation password to register for a new account. It will show a warning if user doesn't input proper information (not inputting a username/password/confirmation password, inputting a username that is already taken, etc.)

**home.html** displays the index / homepage of the project. This page shows a table of all tasks whose 'completed' aspect is labeled as False (0), as well as what time those tasks were created. It also allows a user to select several tasks and press a 'Complete Tasks' button to mark these tasks as completed.

**newtask.html** shows a page where a user can input a task into a text field. It shows a warning if the text field is left blank. When the user submits a new task, the app will redirect the user to the homepage, where their new task will now display

**completed.html** is like the homepage, but displays completed tasks (tasks whose 'completed' field is labeled as True (1)) instead of uncompleted tasks. It also displays what date and time a user completed a task. In case a user accidentally marked a task as completed, they can select one or more tasks and revert them back to an uncomplete status, and those tasks will again display on the homepage

**shakespeare.html** shows an easteregg page. This page can be accessed through clicking the picture of Shakespeare in the navbar. At the top is the title of the web app, and below it is a block quote written in the style of shakespeare. At the bottom shows the originator of the quote, with a link.