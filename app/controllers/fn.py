from flask import Flask
from app import db
from app.models.models import User, Club, Age, Category, Tag, Photo
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, contains_eager, session
from pprint import pprint

def format_tags(tags_list):
    tags_list = tags_list.replace(',','')
    tags_list = tags_list.split()
    return tags_list

def format_form_list(item_dict):
    item_list = []
    for i in item_dict:
        if str(item_dict[i]) == 'True':
            item_list.append(str(i))
    return item_list

#Функция поиска с Главной странице по одной строке
def SimpleSearch(search_value):
    clubs = Club.query.join(Club.tags, aliased=True).filter(Tag.name.like('%' + search_value + '%'))
    return clubs

#Функция поиска возраста определенного клуба
def AgeSearch(club_id):
    club_ages = Age.query.join(Age.clubs, aliased=True).filter(Club.id == club_id).all()
    return club_ages