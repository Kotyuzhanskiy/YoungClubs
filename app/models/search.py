from flask import render_template, flash, redirect, url_for

def search():
    # TO DO
    flash('Search for sucsessful')
    return render_template('search.html', title='Результаты поиска учреждений')