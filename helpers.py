
from flask import redirect, session
from functools import wraps
import re


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# email validation
def is_valid_email(email):
    return bool(re.match(r'\b[A-Za-z0-9._%=-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email))


# password validation
def is_valid_password(password):
    if len(password) > 5:
        lower_case = False
        upper_case = False
        num = False
        special = False
        for char in password:
            if char.isdigit():
                num = True
            if char.islower():
                lower_case = True
            if char.isupper():
                upper_case = True
            if not char.isalnum():
                special = True
        return lower_case and upper_case and num and special
    else:
        return False


def usd(value):
    """Format value as USD."""
    return f"${float(value):,.2f}"
