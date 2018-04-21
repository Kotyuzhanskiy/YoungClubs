from flask import Flask
from app import db
from app.models.models import User, Club, Age, Category, Tag, Photo
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
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
    x = Club.query.filter(Club.tags.any(name=search_value)).all()
    #x = Club.query.filter(Club.tags.like(name=search_value)).all()
    return x
#Функция расширенного поиска по различным полям (категория, возраст, тэги)
def AdvancedSearch(search_value):
    print('f')

