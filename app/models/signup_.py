import os
import smtplib

from flask import render_template, flash, redirect, url_for
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///clubs.db")

def signup():
     """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        pass_word = request.form.get("password")
        email = request.form.get("email")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not pass_word:
            return apology("must provide password", 400)

        # Ensure e-mail was submitted
        elif not email:
            return apology("must provide email", 400)

        if len(pass_word) < 6:
            return apology("lenght of password < 6", 400)
        if not pass_word.isalnum():
            return apology("password doesn't consist only letters or numbers", 400)

        if pass_word != request.form.get("confirmation"):
            return apology("passwords don't match", 400)


       # Query database for username
        hash = generate_password_hash(pass_word, method='pbkdf2:sha256', salt_length=8)
        rows = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                           username=username, hash=hash)
        if not rows:
            return apology("username already exist. try again.", 400)

#   !!!  E MAIL  !!!
        message = "You are registered!"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("youngclubs2018@gmail.com", ">ysqRke,")
        #(from, to, message)
        server.sendmail("youngclubs2018@gmail.com", email, message)

        # Redirect user to home page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template('signup.html', title='Зарегистрироваться')