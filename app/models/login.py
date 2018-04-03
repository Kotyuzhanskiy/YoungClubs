from flask import render_template, flash, redirect, url_for
from controllers.forms import LoginForm
from account import account

def login():
    # TO DO
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('account'))
    return render_template('login.html', title='Войти', form=form)