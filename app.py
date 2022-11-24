# FLASK INSTALLATION NOTES:
# First make sure python and pip are installed.
# Then run pip install flask.
# Make sure python interpreter matches python version in bottom right.
"""
Imports
"""
from flask import Flask, render_template, redirect, request

# configure application
app = Flask("__name__")


"""
Routes
"""


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/tips", methods=["GET", "POST"])
def log():
    if request.method == "POST":
        return redirect("/log.html")
    else:
        return render_template("/templates/log.html")


@app.route("/odds", methods=["GET", "POST"])
def odds():

    return render_template("/templates/odds.html")


@app.route("/tips", methods=["GET", "POST"])
def tips():

    return render_template("/templates/tips.html")


if __name__ == "__main__":
    app.run()
