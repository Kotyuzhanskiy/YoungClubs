import os
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify, send_from_directory
from app import app
from app.controllers.forms import LoginForm, SearchForm, SignUpForm, AdvancedSearchForm, AddClubForm
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from app.models.models import User, Club, Category, Tag
from werkzeug.utils import secure_filename
from app import db
from app.controllers.fn import format_tags, format_form_list, SimpleSearch, SimpleSearch2
from pprint import pprint

###       ПОМЕНЯТЬ ПУТЬ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

UPLOAD_FOLDER_LOG = '/home/ubuntu/workspace/YouthClubs/app/logo/'
UPLOAD_FOLDER_PHOTO = '/home/ubuntu/workspace/YouthClubs/app/photo/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER_LOG'] = UPLOAD_FOLDER_LOG
app.config['UPLOAD_FOLDER_PHOTO'] = UPLOAD_FOLDER_PHOTO
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#Главная страница
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    return render_template('index.html', title='Добро пожаловать', form=form)

#Страница найденных результатов поиска
@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        search_value = form.search.data
        (clubs_search_results, n) = SimpleSearch(search_value)
        pprint(n)
        return render_template(
            'search.html', title='Результаты поиска учреждений',
            clubs_search_results=clubs_search_results, search_value=search_value, n=n
            )
    return render_template('search.html', title='Результаты поиска учреждений')

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
    user_select = db.engine.execute("SELECT * FROM clubs WHERE user_id = :user_id", user_id=current_user.id).fetchall()
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
            institution=form.institution.data,
            ages_from=form.ages_from.data,
            ages_to=form.ages_to.data
            )
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
        #new_age_list = format_form_list(form.ages.data)
        #for age in new_age_list:
        #    row = Age.query.filter_by(name=age).first()
        #    if row == None:
        #        new_age = Age(name=age)
        #        db.session.add(new_age)
        #        new_club.ages.append(new_age)
        #    else:
        #        new_club.ages.append(row)
        db.session.commit()#Подтверждение записи в таблицы БД
        return render_template('addlogo.html')
    return render_template('addclub.html', title='Добавление нового кружка', form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/addlogo', methods=['GET', 'POST'])
@login_required
def addlogo():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_LOG'], filename))
        else:
            filename = 'logo-ghostbuster.jpg'
        last_id = db.engine.execute("SELECT MAX(id) FROM clubs").fetchone()[0]
        db.engine.execute("UPDATE clubs SET url_logo=:url_logo WHERE id = :id", id=last_id, url_logo=filename)
#        print('file=', filename)
        uploads(filename)
#        print('up_file=')
        return render_template('addlogo.html')
#        return redirect(url_for('account'))
#    else:
#        print('222222222222')
#        return render_template('addlogo.html')

@app.route('/addphoto', methods=['GET', 'POST'])
@login_required
def addphoto():
    if request.method == 'POST':
        last_id = db.engine.execute("SELECT MAX(id) FROM clubs").fetchone()[0]
        print('-------')
        file1 = request.files['file1']
        print('file1=', file1)
        if file1 and allowed_file(file1.filename):
            filename1 = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER_PHOTO'], filename1))
        else:
            filename1 = 'logo-ghostbuster.jpg'
#        return render_template('addlogo.html')

        file2 = request.files['file2']
        if file2 and allowed_file(file2.filename):
            filename2 = secure_filename(file2.filename)
            file2.save(os.path.join(app.config['UPLOAD_FOLDER_PHOTO'], filename2))
        else:
            filename2 = 'logo-ghostbuster.jpg'

        file3 = request.files['file3']
        if file3 and allowed_file(file3.filename):
            filename3 = secure_filename(file3.filename)
            file3.save(os.path.join(app.config['UPLOAD_FOLDER_PHOTO'], filename3))
        else:
            filename3 = 'logo-ghostbuster.jpg'

        db.engine.execute("""UPDATE clubs SET url_photo_1=:photo1, url_photo_2=:photo2, url_photo_3=:photo3 WHERE id = :id"""
        , id=last_id, photo1=filename1, photo2=filename2, photo3=filename3)
#        print('file=', filename)
        photo(filename1)
        photo(filename2)
        photo(filename3)
#        print('up_file=')
        return redirect(url_for('account'))

@app.route('/uploads/<filename>')
def uploads(filename):
    print('upload')
    return send_from_directory(app.config['UPLOAD_FOLDER_LOG'], filename)

@app.route('/photo/<filename>')
def photo(filename):
    print('upload_photo')
    return send_from_directory(app.config['UPLOAD_FOLDER_PHOTO'], filename)

@app.route('/editclub/<club_id>', methods=['GET'])
@login_required
def editclub(club_id):
    club = db.engine.execute("SELECT * FROM clubs WHERE id = :club_id", club_id = club_id).fetchall()[0]
    return render_template('editclub.html', title='Управление кружками пользователя', club=club)

@app.route('/deleteclub/<club_id>', methods=['GET'])
@login_required
def deleteclub(club_id):
    club_del = db.engine.execute("DELETE FROM clubs WHERE id = :club_id", club_id = club_id)
    return redirect (url_for('account'))

@app.route('/updateclub', methods=['POST'])
@login_required
def updateclub():
    id = request.form.get('id')
    name = request.form.get('name')
    institution = request.form.get('institution')
    leader = request.form.get('leader')
    price = request.form.get('price')
    snippet = request.form.get('snippet')
    description = request.form.get('description')
    phone = request.form.get('phone')
    web = request.form.get('web')
    email = request.form.get('email')
    social = request.form.get('social')
    street = request.form.get('street')
    building = request.form.get('building')
    room = request.form.get('room')
    club_update = db.engine.execute(
        """
            UPDATE clubs SET name=:name, institution=:institution, leader=:leader,
            price=:price, snippet=:snippet, description=:description, phone=:phone, web=:web, email=:email,
            social=:social, street=:street, building=:building, room=:room
            WHERE id = :id
        """
        , id = id, name=name, institution=institution, leader=leader, price=price, snippet=snippet, description=description, phone=phone, web=web, email=email,
            social=social, street=street, building=building, room=room)
    return redirect (url_for('account'))

@app.route('/club/<club_id>', methods=['GET'])
def getclub(club_id):
    club = db.session.query(Club).filter(Club.id == club_id).all()
    #club_ages = AgeSearch(club_id)
    #club = db.engine.execute("SELECT * FROM clubs WHERE id = :club_id", club_id = club_id).fetchall()[0]
    return render_template('getclub.html', title='Информация о кружке', club=club)

