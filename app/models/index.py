from flask import render_template, flash, redirect, url_for
from app.controllers.forms import SearchForm
from app.models.search import search

def index():
    # TO DO
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search'))
    return render_template('index.html', title='Welcome', form=form)