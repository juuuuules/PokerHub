# FLASK INSTALLATION NOTES:
# First make sure python and pip are installed.
# Then run pip install flask.
# Make sure python interpreter matches python version in bottom right.
"""
Imports
"""
import sqlite3
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

from helpers import login_required, is_valid_email, is_valid_password

# OPEN SOURCE TOOLS
# 1 - unsplash (open-source images)
# 2 - coverr (open-source video)
# 3 - google fonts (free fonts)
# 4 - flaticon (any icon you want)

# configure application
app = Flask("__name__")

# configure session to use filesystem instead of cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# configure database
conn = sqlite3.connect("poker.db", check_same_thread=False)
db = conn.cursor()


"""
Routes
"""


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/log", methods=["GET", "POST"])
# NOTE: FOR THE TIME BEING, making this NOT login required and making it show up in initial nav-bar.
# CHANGE LATER.
def log():
    # add to session history
    if request.method == "POST":

        return redirect("/log")

    # display session and hand history
    user_id = session["user_id"]
    sessions = db.execute("SELECT * FROM sessions WHERE user_id = ?", user_id)
    hands = db.execute("SELECT * FROM hands WHERE user_id = ?", user_id)
    return render_template("log.html", sessions=sessions, hands=hands)


@app.route("/odds", methods=["GET", "POST"])
@login_required
def odds():
    return render_template("/templates/odds.html")


@app.route("/tips", methods=["GET", "POST"])
@login_required
def tips():
    return render_template("/templates/tips.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        error_message = ""
        if email == "" or password == "":
            error_message = "Please fill out the required fields"
            return render_template("login.html", error_message=error_message)

        # Query database for email
        rows = db.execute("SELECT * FROM users WHERE email = ?", email)

        # ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            error_message = "Please check your email and password."
            return render_template("login.html", error_message=error_message)
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        error_message = ""

        if email == "" or password == "" or confirmation == "":
            error_message = "Please fill out the required fields"
            return render_template("register.html", error_message=error_message)

        elif not is_valid_email(email):
            error_message = "Please enter a valid email address"
            return render_template("register.html", error_message=error_message)

        elif not is_valid_password(password):
            error_message = "Password must be at least 5 characters long and contain at least one number, one upper case letter, one lower case letter, and one special character."
            return render_template("register.html", error_message=error_message)

        elif password != confirmation:
            error_message = "Passwords do not match."
            return render_template("register.html", error_message=error_message)

        # check if user already exists
        #
        rows = db.execute(
            "SELECT * FROM users WHERE email = ?", (email,)).fetchall()
        if len(rows) > 0:
            error_message = "There is already an account registered with that email address."
            return render_template("register.html", error_message=error_message)

        # calculate password hash
        hash = generate_password_hash(password)

        # add user to database
        db.execute("INSERT INTO users (email, hash) VALUES (?, ?)",
                   (email, hash))
        print(email, hash)
        return redirect("/")

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
