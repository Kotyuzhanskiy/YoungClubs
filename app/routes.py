# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app
from app.controllers.forms import LoginForm, SearchForm, SignUpForm, AdvancedSearchForm, AddClubForm, CityForm
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from app.models.models import User, Club, Age, Category, Tag, Photo
from app import db
from app.controllers.fn import format_tags, format_form_list, SimpleSearch, AdvancedSearch
from pprint import pprint

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
    form2 = AdvancedSearchForm()
    search_value = form.search.data
    if form.validate_on_submit():
        clubs_search_results = SimpleSearch(search_value)
        for club in clubs_search_results:
            print(club.id)
            print(club.name)
            print(club.snippet)
        #return render_template('search.html', title='Результаты поиска учреждений', form2=form2)
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
    #выбор из clubs и institution. похожие названия колонок переименовывать "i.name as name_i"
    #user_select = db.engine.execute("SELECT c.*, i.name as name_i FROM clubs c INNER JOIN institutions i ON c.institution_id = i.id WHERE user_id = :user_id", user_id=current_user.id)
    user_select = db.engine.execute("SELECT * FROM clubs WHERE user_id = :user_id", user_id=current_user.id)
    return render_template('account.html', title='Управление кружками пользователя', user_select=user_select)

#Страница регистрации пользователя из детских учреждений
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
            #start=form.start.data,
            #finish=form.finish.data,
            url_logo=form.url_logo.data,
            institution=form.institution.data
            #photos=form.photos.data,
            )
        #new_institution = Institution(
        #    name=form.institution.data
        #    )
        db.session.add(new_club)
        #db.session.add(new_institution)
        #new_institution.clubs.append(new_club)
        db.session.add(new_club)
        #Добавление тэгов для клуба в БД
        new_tags_list = format_tags(form.tags.data)
        for tag in new_tags_list:
            row = Tag.query.filter_by(name=tag).first()
            if row == None:
                new_tag = Tag(name=tag)
                db.session.add(new_tag)
                new_club.tags.append(new_tag)
            else:
                new_club.tags.append(row)
        #Добавление категории для кружка в БД
        new_category_list = format_form_list(form.categories.data)
        for category in new_category_list:
            row = Category.query.filter_by(name=category).first()
            if row == None:
                new_category = Category(name=category)
                db.session.add(new_category)
                new_club.categories.append(new_category)
            else:
                new_club.categories.append(row)
        #Добавление возрастов для кружка в БД
        new_age_list = format_form_list(form.ages.data)
        for age in new_age_list:
            row = Age.query.filter_by(name=age).first()
            if row == None:
                new_age = Age(name=age)
                db.session.add(new_age)
                new_club.ages.append(new_age)
            else:
                new_club.ages.append(row)
        #Добавление времени работы для кружка в БД
        db.session.commit()#Подтверждение записи в таблицы БД
        return redirect(url_for('account'))
    return render_template('addclub.html', title='Добавление нового кружка', form=form)

@app.route('/editclub/<club_id>', methods=['GET'])
@login_required
def editclub(club_id):
    club = db.engine.execute("SELECT * FROM clubs WHERE id = :club_id", club_id = club_id)
    return render_template('editclub.html', title='Управление кружками пользователя', club=club)

@app.route('/deleteclub/<club_id>', methods=['GET'])
@login_required
def deleteclub(club_id):
    club_del = db.engine.execute("DELETE FROM clubs WHERE c.id =  = :club_id", club_id = club_id)
    return redirect (url_for('account'))

@app.route('/updateclub/<club_id>', methods=['GET'])
@login_required
def updateclub(club_id):
    club_update = db.engine.execute("UPDATE clubs SET WHERE c.id =  = :club_id", club_id = club_id)
    return redirect (url_for('account'))