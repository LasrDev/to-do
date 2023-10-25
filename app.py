from functools import wraps
from xml.dom.domreg import registered
from flask import Flask, redirect, render_template, request, session, g, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime
import time
import sqlite3
import os.path


# Configure Application
app = Flask(__name__)

# Ensure templates are auto-reloaoded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Login Reqired
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    has_registered = False
    if request.method == 'POST':

        # Use Information Database
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "information.db")

        # User inputted values
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")


        """Check if user submits correct info"""

        # Make sure user submits username
        if not username:
            return render_template('register.html', username_alert=True)

        # Make sure username user has submitted does not already exist
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            for i in range(cursor.execute('SELECT COUNT(username) FROM users').fetchone()[0]):
                if username == cursor.execute('SELECT username FROM users').fetchall()[i][0]:
                    return render_template('register.html', already_exists=True)

        # Make sure user submits password
        if not password:
            return render_template('register.html', password_alert=True)

        # Make sure user confirms password
        if not confirmation:
            return render_template('register.html', confirmation_alert=True)

        # Make sure confirmation input matches password
        if confirmation != password:
            return render_template('register.html', match_alert=True)


        """Once all checks are passed, add new user"""

        # Hash password
        passhash = generate_password_hash(password)

        # Insert new user into database
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (
                            username,
                            passhash
                            ))

        # Person has registered
        return render_template('register.html', has_registered=True)

    else:
        return render_template('register.html')


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    # Use Information Database
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "information.db")
    
    if request.method == "POST":

        # Forget any user id
        session.clear()

        # Access form data
        username = request.form.get("username")
        password = request.form.get("password")

        # For Loop Counting
        user_count = 0


        """Check if login info is correct"""

        # Check if username is inputted
        if not username:
            return render_template('login.html', username_alert=True)
        
        # Check if password is inputted
        if not password:
            password_alert = True
            return render_template('login.html', password_alert=True)

        # Check inputs
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            count = cursor.execute('SELECT COUNT(username) FROM users').fetchone()[0]

            # Check if user exsists
            for i in range(count):
                if username == cursor.execute('SELECT username FROM users').fetchall()[i][0]:

                    # User is found, check if password matches
                    if check_password_hash(cursor.execute('SELECT hash FROM users WHERE username = ?', (username,)).fetchone()[0], password):

                        # Password matches, log user in
                        session['user_id'] = cursor.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()[0]
                        return redirect("/")

                    else:
                        # Password doesn't match
                        return render_template('login.html', doesnt_match=True)
                else:
                    user_count += 1
            
            if user_count == count:
                return render_template('login.html', doesnt_exist=True)
    else:
        return render_template('login.html')


# Quote Page
@app.route("/shakespeare")
def shakespeare():
    return render_template('shakespeare.html')


# Add a New Task Page
@app.route("/newtask", methods=["GET", "POST"])
@login_required
def newtask():
    if request.method == 'POST':
        # Datetime stuff
        create_date = time.strftime('%Y-%m-%d %H:%M:%S')
        task = request.form.get("newtask")
        print(task)

        # Use Information Database
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "information.db")

        # Check if text box is blank
        if not task:
            return render_template('newtask.html', alert=True)

        # Insert task into table
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()

            cursor.execute("INSERT INTO tasks (user_id, task_string, date_created) VALUES (?, ?, ?)", (
                        session['user_id'],
                        task,
                        create_date
                        ))

        return redirect('/')

    else:
        return render_template('newtask.html')


@app.route("/", methods=["GET", "POST"])
@login_required
def index(): 
    # Use Information Database
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "information.db")

    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()

        # Variables
        count = cursor.execute('SELECT COUNT(*) FROM tasks WHERE user_id = ? AND completed = False', (session['user_id'],)).fetchone()
        task = cursor.execute("SELECT task_string FROM tasks WHERE user_id = ? AND completed = False", (session['user_id'],)).fetchall()
        task_id = cursor.execute('SELECT task_id FROM tasks WHERE user_id = ? AND completed = False', (session['user_id'],)).fetchall()
        date_created = cursor.execute('SELECT date_created FROM tasks WHERE user_id = ? AND completed = False', (session['user_id'],)).fetchall()

    if request.method == 'POST':
        task_completed = request.form.getlist("task")
        task_count = len(task_completed)

        # Check if user selected anything
        if not task_completed:
            return render_template('home.html',
                                    count=count[0],
                                    task=task,
                                    task_id=task_id,
                                    date_created=date_created,
                                    no_task=True
                                  )

        # Mark tasks as 'completed'
        for i in range(task_count):
            complete_date = time.strftime('%Y-%m-%d %H:%M:%S')
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                cursor.execute('UPDATE tasks SET completed = True, date_completed = ? WHERE user_id = ? AND task_id = ?', (
                                complete_date,
                                session['user_id'],
                                task_completed[i]
                                ))
    
        return redirect("/")

    else:
        return render_template('home.html',
                                count=count[0],
                                task=task,
                                task_id=task_id,
                                date_created=date_created
                              )


@app.route("/completed", methods=['GET', 'POST'])
@login_required
def completed():
    # Use Information Database
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "information.db")

    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()

        # Variables
        count = cursor.execute('SELECT COUNT(*) FROM tasks WHERE user_id = ? AND completed = True', (session['user_id'],)).fetchone()
        task = cursor.execute("SELECT task_string FROM tasks WHERE user_id = ? AND completed = True", (session['user_id'],)).fetchall()
        task_id = cursor.execute('SELECT task_id FROM tasks WHERE user_id = ? AND completed = True', (session['user_id'],)).fetchall()
        date_created = cursor.execute('SELECT date_created FROM tasks WHERE user_id = ? AND completed = True', (session['user_id'],)).fetchall()
        date_completed = cursor.execute('SELECT date_completed FROM tasks WHERE user_id = ? AND completed = True', (session['user_id'],)).fetchall()
        

    if request.method == 'POST':
        tasks = request.form.getlist('task')
        task_count = len(tasks)

        # Check if user selected anything
        if not tasks:
            return render_template('completed.html',
                                    count=count[0],
                                    task=task,
                                    task_id=task_id,
                                    date_created=date_created,
                                    date_completed=date_completed,
                                    no_task=True
                                  )
        
        for i in range(task_count):
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                cursor.execute('UPDATE tasks SET completed = False WHERE user_id = ? AND task_id = ?', (
                                session['user_id'],
                                tasks[i]
                              ))

        return redirect("/")
    else:
        return render_template('completed.html',
                                count=count[0],
                                task=task,
                                task_id=task_id,
                                date_created=date_created,
                                date_completed=date_completed
                              )


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")