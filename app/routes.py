# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from app import app
from app.controllers.forms import LoginForm, SearchForm

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    # TO DO
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search'))
    return render_template('index.html', title='Welcome', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    # TO DO
    flash('Search for sucsessful')
    return render_template('search.html', title='Результаты поиска учреждений')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # TO DO
    #form = LoginForm()
    #if form.validate_on_submit():
    #    flash('Login requested for user {}, remember_me={}'.format(
    #        form.username.data, form.remember_me.data))
    #    return redirect(url_for('account'))
    #return render_template('login.html', title='Войти', form=form)
 
 # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        Name = request.form.get("Name")
        pass_word = request.form.get("password")
        if not Name:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not pass_word:
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM user WHERE Name = :Name", Name=Name)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], pass_word):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")    

@app.route('/account', methods=['GET', 'POST'])
def account():
    #TO DO
    return render_template('account.html', title='Управление кружками пользователя')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # TO DO
    #return render_template('signup.html', title='Зарегистрироваться')

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        Name = request.form.get("Name")
        PatronymicNname = request.form.get("PatronymicNname")
        SurName = request.form.get("SurName")
        pass_word = request.form.get("password")
        email = request.form.get("email")

        # Ensure username was submitted
        if not Name:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not pass_word:
            return apology("must provide password", 400)

        # Ensure e-mail was submitted
        elif not email:
            return apology("must provide email", 400)

     #   if len(pass_word) < 6:
     #       return apology("lenght of password < 6", 400)
     #   if not pass_word.isalnum():
     #       return apology("password doesn't consist only letters or numbers", 400)

        if pass_word != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

       # Query database for username
        password_hash = generate_password_hash(pass_word, method='pbkdf2:sha256', salt_length=8)
        rows = db.execute("INSERT INTO user (Name, PatronymicNname, SurName, email, password_hash) VALUES (:Name, :PatronymicNname, :SurName, :email, :password_hash)",
                           Name=Name, PatronymicNname=PatronymicNname, SurName=SurName, email=email, password_hash=password_hash)
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
    else:
        return render_template("register.html")    

