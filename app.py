# FLASK INSTALLATION NOTES:
# First make sure python and pip are installed.
# Then run pip install flask.
# Make sure python interpreter matches python version in bottom right.
"""
Imports
"""
import sqlite3
from flask import Flask, render_template, redirect, request, session, jsonify
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


"""
Routes
"""
# register user


@app.route("/register", methods=["GET", "POST"])
def register():

    # configure database
    conn = sqlite3.connect("poker.db")
    db = conn.cursor()

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
        conn.commit()

        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    # configure database
    conn = sqlite3.connect("poker.db")
    db = conn.cursor()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        error_message = ""
        if email == "" or password == "":
            error_message = "Please fill out the required fields"
            return render_template("login.html", error_message=error_message)

        # Query database for email
        rows = db.execute(
            "SELECT * FROM users WHERE email = ?", (email,)).fetchall()

        # ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            error_message = "Please check your email and password."
            return render_template("login.html", error_message=error_message)
        session["user_id"] = rows[0][0]

        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/log", methods=["GET", "POST"])
@login_required
def log():
    # configure database
    conn = sqlite3.connect("poker.db")
    db = conn.cursor()

    # add to session history
    if request.method == "POST":
        return redirect("/log")

    # display session and hand history
    user_id = session["user_id"]
    sessions = db.execute(
        "SELECT * FROM sessions WHERE user_id = ?", (user_id,)).fetchall()
    hands = db.execute(
        "SELECT * FROM hands WHERE user_id = ?", (user_id,)).fetchall()
    return render_template("log.html", sessions=sessions, hands=hands)


@app.route("/ajax_add", methods=["POST", "GET"])
def ajax_add():
    conn = sqlite3.connect("poker.db")
    db = conn.cursor()
    if request.method == "POST":
        user_id = session["user_id"]
        session_id = request.form["sessionid"]
        hand = request.form["txthand"]
        result = request.form["txtresult"]
        potsize = request.form["txtpot"]
        print(hand)
        db.execute("INSERT INTO hands (user_id, session_id, user_hand, result, pot_size) VALUES (?,?,?,?, ?)", [
                   user_id, session_id, hand, result, potsize])
        msg = "New Hand Created Successfully"
    return jsonify(msg)


@ app.route("/odds", methods=["GET", "POST"])
@ login_required
def odds():
    return render_template("odds.html")


@ app.route("/tips", methods=["GET", "POST"])
@ login_required
def tips():
    return render_template("tips.html")


if __name__ == "__main__":
    app.run(debug=True)
