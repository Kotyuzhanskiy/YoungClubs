from flask import render_template
from app.controllers.forms import CityForm

def city():
    # TO DO
    form = CityForm()
    return render_template('city.html', title='Welcome', form=form)