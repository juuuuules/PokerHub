# FLASK INSTALLATION NOTES:
# First make sure python and pip are installed.
# Then run pip install flask.
# Make sure python interpreter matches python version in bottom right.
"""
Imports
"""
from flask import Flask, render_template, redirect, request, session
from flask_session import Session

from helpers import login_required
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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tips", methods=["GET", "POST"])
@login_required
def log():
    if request.method == "POST":
        return redirect("/log")
    else:
        return render_template("/templates/log.html")


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
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    pass


if __name__ == "__main__":
    app.run(debug=True)
