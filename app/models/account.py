from flask import render_template, flash, redirect, url_for

def account():
    #TO DO
    return render_template('account.html', title='Управление кружками пользователя')