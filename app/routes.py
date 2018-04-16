# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.controllers.forms import LoginForm, SearchForm, SignUpForm, AdvancedSearchForm, AddClubForm, CityForm
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from app.models.models import User, Club, Institution, Age, Category, Tag, Photo
from app import db

#Функция загрузки других функций при отображении любой страницы
#@app.before_request
#def before_request():
#    cityform = CityForm()
#    print('--------------DEBUG-1--------------')
#    print(cityform)
#    return CityForm()

#@app.context_processor
#def utility_processor(methods=['GET', 'POST']):
#    cityform = CityForm()
#    return dict(cityform=cityform)

#Главная страница
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    # TO DO
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search'))
    return render_template('index.html', title='Добро пожаловать', form=form)

#Страница найденных результатов поиска
@app.route('/search', methods=['GET', 'POST'])
def search():
    # TO DO
    flash('Search for sucsessful')
    form = AdvancedSearchForm()
    return render_template('search.html', title='Результаты поиска учреждений', form=form)

#Страница входа для зарегистрированных пользователей из детских учреждений
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

#Функция выхода зарегистрированного пользователя из приложения
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#Страница аккаунта зарегистрированного пользователя для управления его кружками
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user_select = Club.query.filter_by(user_id=current_user.id).all()
    return render_template('account.html', title='Управление кружками пользователя', user_select=user_select)

#Страница зарегистрации пользователя из детских учреждений
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

#Страница (функция?) добавления кружка зарегистрированным пользователем
@app.route('/addclub', methods=['GET', 'POST'])
@login_required
def addclub():
    #TO DO
    form = AddClubForm()
    if form.validate_on_submit():
        new_club = Club(
            user_id=current_user.id,
            name=form.name.data,
            snippet=form.snippet.data,
            description=form.description.data,
            leader=form.leader.data,
            price=form.price.data,
            phone=form.phone.data,
            web=form.web.data,
            email=form.email.data,
            social=form.social.data,
            street=form.street.data,
            building=form.building.data,
            room=form.room.data,
            days=form.days.data,
            start=form.start.data,
            finish=form.finish.data,
            url_logo=form.url_logo.data,
            #photos=form.photos.data,
            )
        new_institution = Institution(
            name=form.institution.data
            )
        new_ages = Age(
            age_from=form.age_from.data,
            age_to=form.age_to.data
            )
        #catagories = ', '.join([f'{key}: {value}' for key, value in form.categories.data.keys()])
        #print('----------------DEBUG----------------')
        #print(catagories)
        #new_categories = Category(# добавление категории
        #    name=catagories
        #    )
        new_tags = Tag(
            name=form.tags.data
            )
        #new_photos = Photo(
        #    url=form.photos.data
        #    )
        db.session.add(new_club)
        db.session.add(new_institution)
        db.session.add(new_ages)
        #db.session.add(new_categories) # добавление категории
        db.session.add(new_tags)
        new_institution.clubs.append(new_club)
        new_club.ages.append(new_ages)
        #new_club.categories.append(new_categories) # добавление категории
        new_club.tags.append(new_tags)
        #new_photos.club.append(new_club)
        db.session.add(new_club)
        db.session.commit()
        return redirect(url_for('account'))
    return render_template('addclub.html', title='Добавление нового кружка', form=form)