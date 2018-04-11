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

    #Таблица кружков
class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), index=True, unique=False)
    snippet = db.Column(db.String(300), index=False, unique=False)
    description = db.Column(db.String(2000), index=False, unique=False)
    price = db.Column(db.String(100), index=False, unique=False)
    phonefix = db.Column(db.String(10), index=False, unique=False)
    phonemob = db.Column(db.String(10), index=False, unique=False)
    web = db.Column(db.String(120), index=False, unique=False)
    email = db.Column(db.String(120), index=False, unique=False)
    social = db.Column(db.String(120), index=False, unique=False)
    building = db.Column(db.String(5), index=False, unique=False)
    room = db.Column(db.String(5), index=False, unique=False)
    days = db.Column(db.String(50), index=False, unique=False)
    start = db.Column(db.String(50), index=False, unique=False)
    finish = db.Column(db.String(50), index=False, unique=False)
    url_logo = db.Column(db.String(300), index=False, unique=False)
    #отношение к таблице Insitution n:1
    insitution_id = db.Column(db.Integer, db.ForeignKey('institution.id'))
    institution = db.relationship('Institution', backref='institution', lazy='dynamic')
    #отношение к таблице City n:1
    city_id = db.Column(db.Integer, db.ForeignKey('city.id')) #n:1
    city = db.relationship('City', backref='city', lazy='dynamic')
    #отношение к таблице Street n:1
    street_id = db.Column(db.Integer, db.ForeignKey('street.id')) #n:1
    street = db.relationship('Street', backref='street', lazy='dynamic')
    #отношение к таблице Photo 1:n
    photo = db.relationship('Photo', backref='photo', lazy='dynamic')
    #отношение к таблице Video 1:n
    video = db.relationship('Video', backref='video', lazy='dynamic')
    #отношение к таблице Leaders m:n

    #Таблица учреждений
class Insitution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), index=True, unique=False)
    #отношение к таблице Club 1:n
    club = db.relationship('Club', back_populates="institution", lazy='dynamic')

    #Таблица городов
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), index=True, unique=False)
    #отношение к таблице Club 1:n
    club = db.relationship('Club', back_populates="city", lazy='dynamic')

    #Таблица улиц
class Street(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), index=True, unique=False)
    #отношение к таблице Club 1:n
    club = db.relationship('Club', back_populates="street", lazy='dynamic')

    #Таблица фото
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(300), index=False, unique=False)
    #отношение к таблице Club n:1
    club_id = Column(Integer, ForeignKey('club.id'))
    club = relationship("Club", back_populates="club", lazy='dynamic')

    #Таблица видео
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(300), index=False, unique=False)
    #отношение к таблице Club n:1
    club_id = Column(Integer, ForeignKey('club.id'))
    club = relationship("Club", back_populates="club", lazy='dynamic')

    #Таблица руководителей (преподавателей) кружка
class Leader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), index=False, unique=False)
    #отношение к таблице Club n:m
