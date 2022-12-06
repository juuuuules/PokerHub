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

from helpers import login_required, is_valid_email, is_valid_password, usd, apology, percentage

from eval import simulate
# OPEN SOURCE TOOLS
# 1 - unsplash (open-source images)
# 2 - coverr (open-source video)/
# 3 - google fonts (free fonts)
# 4 - flaticon (any icon you want)

# configure application
app = Flask("__name__")

# Custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem instead of cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


# list of possible cards
deck = ["2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "Th", "Jh", "Qh", "Kh", "Ah", "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "Td", "Jd", "Qd", "Kd",
        "Ad", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "Ts", "Js", "Qs", "Ks", "As", "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "Tc", "Jc", "Qc", "Kc", "Ac"]

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

        # add sample hand to database
        id = db.execute("SELECT id FROM users WHERE email = ?",
                        (email,)).fetchone()[0]
        db.execute(
            "INSERT INTO hands (user_id, user_hand, result, pot_size) VALUES (?, ?, ?, ?)", [id, 'AKs *SAMPLE HAND', 'WIN', 0.00])
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
    # display session and hand history
    user_id = session["user_id"]
    hands = db.execute(
        "SELECT * FROM hands WHERE user_id = ?", (user_id,)).fetchall()

    money_won_total = db.execute(
        "SELECT SUM(pot_size) FROM hands WHERE (user_id = ? AND result = ?)", (user_id, "WIN")).fetchall()[0][0]
    money_lost_total = db.execute(
        "SELECT SUM(pot_size) FROM hands WHERE (user_id = ? AND result = ?)", (user_id, "LOSS")).fetchall()[0][0]
    if money_won_total is None:
        money_won_total = 0
    if money_lost_total is None:
        money_lost_total = 0
    winnings = money_won_total - money_lost_total
    hands_won = db.execute(
        "SELECT user_hand, SUM(pot_size) FROM hands WHERE result = ? AND user_id = ? GROUP BY user_hand", ("WIN", user_id)).fetchall()
    hands_lost = db.execute(
        "SELECT user_hand, SUM(pot_size) FROM hands WHERE result = ? AND user_id = ? GROUP BY user_hand", ("LOSS", user_id)).fetchall()
    best_hands = hands_won
    won_index_count = -1
    biggest_win = 0
    best_hand = None
    for won_hands in hands_won:
        won_index_count += 1
        in_both = False
        for lost_hands in hands_lost:
            if won_hands[0] == lost_hands[0]:
                in_both = True
                current_hand = list(best_hands[won_index_count])
                current_hand[1] = float(won_hands[1]) - float(lost_hands[1])
                best_hands[won_index_count] = tuple(current_hand)
                if current_hand[1] > biggest_win:
                    biggest_win = current_hand[1]
                    best_hand = current_hand[0]
        if in_both == False and won_hands[1] > biggest_win:
            biggest_win = won_hands[1]
            best_hand = won_hands[0]
    worst_hands = hands_lost
    lost_index_count = -1
    biggest_loss = 0
    worst_hand = None
    for lost_hands in hands_lost:
        won_index_count += 1
        in_both = False
        for won_hands in hands_won:
            if lost_hands[0] == won_hands[0]:
                in_both = True
                current_hand = list(worst_hands[lost_index_count])
                current_hand[1] = float(lost_hands[1]) - float(won_hands[1])
                worst_hands[lost_index_count] = tuple(current_hand)
                if current_hand[1] < biggest_loss:
                    biggest_loss = current_hand[1]
                    worst_hand = current_hand[0]
        if in_both == False and lost_hands[1] < biggest_loss:
            biggest_loss = lost_hands[1]
            worst_hand = lost_hands[0]

    if request.method == "POST":
        # get win percentage given hand

        cards = request.form.get("cards")
        # check if cards are blank
        if cards == "":
            error_message = "Please enter a hand."
            return render_template("log.html", hands=hands, total_winnings=winnings, convert_to_usd=usd, percentage=percentage)

        # check if hand exists
        elif len(db.execute(
                "SELECT * FROM hands WHERE user_hand = ?", (cards,)).fetchall()) == 0:
            error_message = "You have not played ths hand."
            return render_template("log.html", hands=hands, total_winnings=winnings, convert_to_usd=usd, percentage=percentage)
        else:
            wins = db.execute(
                "SELECT COUNT(*) FROM hands WHERE (user_id = ? AND user_hand = ? AND result = ?)", (user_id, cards, "WIN")).fetchall()[0][0]
            losses = db.execute(
                "SELECT COUNT(*) FROM hands WHERE (user_id = ? AND user_hand = ? AND result = ?)", (user_id, cards, "LOSS")).fetchall()[0][0]
            print(f"Losses: {losses}")
            print(f"wins: {wins}")

            p = 100 * (wins / (wins + losses))

            money_won_hand = db.execute(
                "SELECT SUM(pot_size) FROM hands WHERE (user_id = ? AND user_hand = ? AND result = ?)", (user_id, cards, "WIN")).fetchall()[0][0]
            money_lost_hand = db.execute(
                "SELECT SUM(pot_size) FROM hands WHERE (user_id = ? AND user_hand = ? AND result = ?)", (user_id, cards, "LOSS")).fetchall()[0][0]
            if money_won_hand is None:
                money_won_hand = 0
            if money_lost_hand is None:
                money_lost_hand = 0
            hand_earnings = money_won_hand - money_lost_hand

            error_message = "Succcess!"
        return render_template("log.html", error_message=error_message, hands=hands, total_winnings=winnings, win_percentage=p, hand_earnings=hand_earnings, convert_to_usd=usd, percentage=percentage)
    return render_template("log.html", hands=hands, total_winnings=winnings, best_hand=best_hand, worst_hand=worst_hand, convert_to_usd=usd, percentage=percentage)


@app.route("/ajax_add", methods=["POST", "GET"])
def ajax_add():
    # configure database
    conn = sqlite3.connect("poker.db")
    db = conn.cursor()
    if request.method == "POST":
        user_id = session["user_id"]
        hand = request.form["txthand"]
        result = request.form["txtresult"].upper()
        potsize = request.form["txtpot"]
        if hand == "":
            msg = "Please input a hand."
        elif result == "":
            msg = "Please input a result."
        elif potsize == "":
            msg = "Please input the size of the pot."
            print(potsize)
        elif not potsize.isnumeric():
            msg = "Please input a numerical value for the size of the pot"
        else:
            db.execute("INSERT INTO hands (user_id, user_hand, result, pot_size) VALUES (?,?,?,?)", [
                user_id, hand, result, potsize])
            conn.commit()
            msg = "New Hand Created Successfully."
    return jsonify(msg)


@app.route("/ajax_update", methods=["POST", "GET"])
def ajax_update():
    # configure database
    conn = sqlite3.connect("poker.db")
    db = conn.cursor()
    if request.method == "POST":
        hand_id = request.form["string"]
        hand = request.form["txthand"]
        result = request.form["txtresult"]
        pot_size = request.form["txtpot"]
        print("---Updated hand---")
        print(f"hand id:  {hand_id}")
        print(f"hand:  {hand}")
        print(f"result: {result}")
        print(f"potsize: {pot_size}")
        if hand == "":
            msg = "Please input a hand."
        elif result == "":
            msg = "Please input a result."
        elif pot_size == "":
            msg = "Please input the size of the pot."
        elif not pot_size.isnumeric():
            msg = "Please input a number for the size of the pot"
        else:
            db.execute("UPDATE hands SET user_hand = ?, result = ?, pot_size = ? WHERE id = ?", [
                hand, result, pot_size, hand_id])
            conn.commit()
            db.close()
            msg = "Hand Updated Successfully."
    return jsonify(msg)


@app.route("/ajax_delete", methods=["POST", "GET"])
def ajax_delete():
    # configure database
    conn = sqlite3.connect("poker.db")
    db = conn.cursor()
    if request.method == "POST":
        getid = request.form["string"]
        print(getid)
        db.execute("DELETE FROM hands WHERE id = {0}".format(getid))
        conn.commit()
        db.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='hands'")
        conn.commit()
        db.close()
        msg = "Hand Deleted Successfully."
    return jsonify(msg)


@ app.route("/odds", methods=["GET", "POST"])
@ login_required
def odds():
    if request.method == "GET":
        return render_template("odds.html")
    else:
        user1 = request.form.get("user1")
        user2 = request.form.get("user2")
        opp1 = request.form.get("opp1")
        opp2 = request.form.get("opp2")
        board1 = request.form.get("board1")
        board2 = request.form.get("board2")
        board3 = request.form.get("board3")
        board4 = request.form.get("board4")
        board5 = request.form.get("board5")
        if not user1 or not user2 or not opp1 or not opp2:
            return apology("Missing Cards")

        if user1 not in deck or user2 not in deck or opp1 not in deck or opp2 not in deck:
            return apology("Invalid Cards")

        # Filtering board cards which are allowed to be left blank
        count = 0
        boardCards = [board1, board2, board3, board4, board5]
        for card in boardCards:
            if card != "" and card not in deck:
                return apology("Invalid Cards")
            elif card in deck:
                count += 1
        # checking if there is a board
        board = False
        if count == 1 or count == 2:
            return apology("Invalid Number of Board Cards")
        elif count >= 3:
            board = True

        chosen_cards = [user1, user2, opp1, opp2,
                        board1, board2, board3, board4, board5]
        # Getting rid of null cards to avoid accidentally triggering repeated card error
        chosen_cards = [card for card in chosen_cards if card != ""]

        if len(set(chosen_cards)) != len(chosen_cards):
            return apology("Repeated Cards")

        # submitting inputs to function
        results = simulate(user1, user2, opp1, opp2, board,
                           board1, board2, board3, board4, board5)
        return render_template("results.html", user1=user1, user2=user2, opp1=opp1, opp2=opp2, results=results, percentage=percentage)


@ app.route("/tips", methods=["GET", "POST"])
@ login_required
def tips():
    return render_template("tips.html")


if __name__ == "__main__":
    app.run(debug=True)
