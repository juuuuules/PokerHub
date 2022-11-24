# FLASK INSTALLATION NOTES:
# First make sure python and pip are installed. 
# Then run pip install flask.
# Make sure python interpreter matches python version in bottom right.
"""
Imports
"""
from flask import Flask, render_template, redirect, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash

# configure application
app = Flask("__name__")


"""
Routes
"""

# home page
@app.route("/")
def index():

    return render_template("index.html")

# log page
@app.route("/tips", methods=["GET", "POST"])
def log():
    if request.method == "POST":
        return redirect("/log.html")
    else:
        return render_template("/templates/log.html")

# odds calculator page
@app.route("/odds", methods=["GET", "POST"])
def odds():
    
    return render_template("/templates/odds.html")

# tips page
@app.route("/tips", methods=["GET", "POST"])
def tips():
    
    return render_template("/templates/tips.html")


if __name__ == "__main__":
    app.run()

