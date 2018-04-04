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
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('account'))
    return render_template('login.html', title='Войти', form=form)

@app.route('/account', methods=['GET', 'POST'])
def account():
    #TO DO
    return render_template('account.html', title='Управление кружками пользователя')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # TO DO
    return render_template('signup.html', title='Зарегистрироваться')

