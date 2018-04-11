# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.controllers.forms import LoginForm, SearchForm, SignUpForm, AdvancedSearchForm, AddClubForm, CityForm
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from app.models.models import User
from app import db

@app.before_request
def before_request():
    cityform = CityForm()
    print('--------------DEBUG-1--------------')
    print(cityform)
    return cityform

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    # TO DO
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search'))
    cityform = CityForm()
    return render_template('index.html', title='Welcome', form=form, cityform=cityform)


@app.route('/search', methods=['GET', 'POST'])
def search():
    # TO DO
    flash('Search for sucsessful')
    form = AdvancedSearchForm()
    cityform = CityForm()
    return render_template('search.html', title='Результаты поиска учреждений', form=form, cityform=cityform)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный пароль или логин')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('account')
        return redirect(next_page)
    return render_template('login.html', title='Войти', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    #TO DO
    return render_template('account.html', title='Управление кружками пользователя')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('account'))
    return render_template('signup.html', title='Зарегистрироваться', form=form)

@app.route('/addclub', methods=['GET', 'POST'])
@login_required
def addclub():
    #TO DO
    form = AddClubForm()
    return render_template('addclub.html', title='Добавление нового кружка', form=form)