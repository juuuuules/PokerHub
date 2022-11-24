# note: to install flask, first make sure python and pip are installed. Then run 
# pip install flask
from flask import Flask, render_template

app = Flask("__name__")


@app.route("/")
def index():
    pass

@app.route("/log.html")
def log():
    pass


if __name__ == "__main__":
    app.run()

