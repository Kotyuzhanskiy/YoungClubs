from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
#Модели базы данных в этом файле представлены набором классов

#Модель базы данных пользователей детских учреждений
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        password_hash = generate_password_hash(password)
        self.password_hash = password_hash[20:]

    def check_password(self, password):
        hash_m = 'pbkdf2:sha256:50000$'
        self.password_hash = hash_m + self.password_hash
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#МОДЕЛЬ БАЗЫ ДАННЫХ ДЕТСКИХ КРУЖКОВ

#ассоциативная таблица для связи Club-Ages
association_table_ages = Table('association_ages', db.metadata,
    Column('clubs_id', Integer, ForeignKey('clubs.id')),
    Column('ages_id', Integer, ForeignKey('ages.id'))
)

#ассоциативная таблица для связи Club-Category
association_table_categories = Table('association_categories', db.metadata,
    Column('clubs_id', Integer, ForeignKey('clubs.id')),
    Column('categories_id', Integer, ForeignKey('categories.id'))
)

#ассоциативная таблица для связи Club-Tags
association_table_tags = Table('association_tags', db.metadata,
    Column('clubs_id', Integer, ForeignKey('clubs.id')),
    Column('tags_id', Integer, ForeignKey('tags.id'))
)

    #Таблица кружков
class Club(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(10), index=True, unique=False)
    name = db.Column(db.String(100), index=True, unique=False)
    snippet = db.Column(db.String(500), index=False, unique=False)
    description = db.Column(db.String(10000), index=False, unique=False)
    leader = db.Column(db.String(150), index=False, unique=False)
    price = db.Column(db.String(50), index=False, unique=False)
    phone = db.Column(db.String(30), index=False, unique=False)
    web = db.Column(db.String(100), index=False, unique=False)
    email = db.Column(db.String(50), index=False, unique=False)
    social = db.Column(db.String(100), index=False, unique=False)
    street = db.Column(db.String(30), index=False, unique=False)
    building = db.Column(db.String(10), index=False, unique=False)
    number = db.Column(db.String(10), index=False, unique=False)
    room = db.Column(db.String(5), index=False, unique=False)
    days = db.Column(db.String(50), index=False, unique=False)
    start = db.Column(db.String(50), index=False, unique=False)
    finish = db.Column(db.String(50), index=False, unique=False)
    url_logo = db.Column(db.String(300), index=False, unique=False)
    reg_date = db.Column(db.Date(), index=True, unique=False)
    last_edit_date = db.Column(db.Date(), index=True, unique=False)
    #отношение к таблице Insitution n:1
    institution_id = db.Column(db.Integer, ForeignKey('institutions.id'))
    institution = relationship("Institution", back_populates='clubs')
    #отношение к таблице Photo 1:n
    photos = relationship("Photo", back_populates='clubs')
    #отношение к таблице Ages n:m
    ages = relationship("Age", secondary=association_table_ages, backref='clubs')
    #отношение к таблице Category n:m
    categories = relationship("Category", secondary=association_table_categories, backref='clubs')
    #отношение к таблице Tags n:m
    tags = relationship("Tag", secondary=association_table_tags, backref='clubs')

    #Таблица учреждений
class Insitution(db.Model):
    __tablename__ = 'institutions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), index=True, unique=False)
    #отношение к таблице Club 1:n
    clubs = relationship('Club', back_populates="institutions")

    #Таблица фото
class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(300), index=False, unique=False)
    #отношение к таблице Club n:1
    club_id = db.Column(db.Integer, ForeignKey('clubs.id'))
    club = db.relationship("Club", back_populates="clubs")

    #Таблица возраста
class Age(db.Model):
    __tablename__ = 'ages'
    id = db.Column(db.Integer, primary_key=True)
    age_from = db.Column(db.Integer, index=False, unique=False)
    age_to = db.Column(db.Integer, index=False, unique=False)

    #Таблица категорий клубов
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=False)

    #Таблица тэгов клубов
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=False)
