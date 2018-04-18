from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

#Модели базы данных в этом файле представлены набором классов

#Модель базы данных пользователей детских учреждений
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    role = db.Column(db.Integer, index=False, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    clubs = db.relationship('Club', back_populates="user", lazy='dynamic')

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
association_table_ages = db.Table('association_ages', db.metadata,
    db.Column('clubs_id', db.Integer, db.ForeignKey('clubs.id')),
    db.Column('ages_id', db.Integer, db.ForeignKey('ages.id'))
)

#ассоциативная таблица для связи Club-Category
association_table_categories = db.Table('association_categories', db.metadata,
    db.Column('clubs_id', db.Integer, db.ForeignKey('clubs.id')),
    db.Column('categories_id', db.Integer, db.ForeignKey('categories.id'))
)

#ассоциативная таблица для связи Club-Tags
association_table_tags = db.Table('association_tags', db.metadata,
    db.Column('clubs_id', db.Integer, db.ForeignKey('clubs.id')),
    db.Column('tags_id', db.Integer, db.ForeignKey('tags.id'))
)

    #Таблица кружков
class Club(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates='clubs')
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
    room = db.Column(db.String(5), index=False, unique=False)
    days = db.Column(db.String(50), index=False, unique=False)
    start = db.Column(db.String(50), index=False, unique=False)
    finish = db.Column(db.String(50), index=False, unique=False)
    url_logo = db.Column(db.String(300), index=False, unique=False)
    reg_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_edit_date = db.Column(db.DateTime, index=True, unique=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))
    institution = db.relationship("Institution", back_populates='clubs')
    ages = db.relationship("Age", secondary=association_table_ages, back_populates='clubs', lazy='dynamic')
    categories = db.relationship("Category", secondary=association_table_categories, back_populates='clubs', lazy='dynamic')
    tags = db.relationship("Tag", secondary=association_table_tags, back_populates='clubs', lazy='dynamic')
    photos = db.relationship("Photo", back_populates="club", lazy='dynamic')

    #Таблица учреждений
class Institution(db.Model):
    __tablename__ = 'institutions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), index=True, unique=False)
    clubs = db.relationship('Club', back_populates="institution")

    #Таблица возраста
class Age(db.Model):
    __tablename__ = 'ages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), index=True, unique=False)
    age_from = db.Column(db.Integer, index=False, unique=False)
    age_to = db.Column(db.Integer, index=False, unique=False)
    clubs = db.relationship("Club", secondary=association_table_ages, back_populates='ages')

    #Таблица категорий клубов
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=False)
    clubs = db.relationship("Club", secondary=association_table_categories, back_populates='categories')

    #Таблица тэгов клубов
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=False)
    clubs = db.relationship("Club", secondary=association_table_tags, back_populates='tags')

    #Таблица фото
class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(300), index=False, unique=False)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))
    club = db.relationship("Club", back_populates="photos")
