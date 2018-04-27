# coding = utf-8
from flask import Flask
from app import db
from app.models.models import User, Club, Category, Tag
from sqlalchemy import Table, Column, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, session
from pprint import pprint
from itertools import groupby

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

#Функция поиска с Главной странице
def SimpleSearch(search_value):
    search_value = search_value.lower()
    clubs_search_results = []
    # поиск по тєгам
    clubs_for_tags = Club.query.join(Club.tags, aliased=True).filter(Tag.name.like('%' + search_value + '%')).all()
    clubs_search_results.extend(clubs_for_tags)
    # поиск по имени
    clubs_for_name = Club.query.filter(func.lower(Club.name).like('%' + search_value + '%')).all()
    clubs_search_results.extend(clubs_for_name)
    # поиск по короткому описанию
    clubs_for_snippet = Club.query.filter(Club.snippet.like('%' + search_value + '%')).all()
    clubs_search_results.extend(clubs_for_snippet)
    # поиск по полному описанию
    clubs_for_description = Club.query.filter(Club.description.like('%' + search_value + '%')).all()
    pprint(type(clubs_search_results))
    pprint(clubs_search_results)
    clubs_search_results = [el for el, _ in groupby(clubs_search_results)]
    n = len(clubs_search_results)
    return clubs_search_results, n

#Функция поиска возраста определенного клуба
#def AgeSearch(club_id):
#    club_ages = Age.query.join(Age.clubs, aliased=True).filter(Club.id == club_id).all()
#    return club_ages

def SimpleSearch2(search_value):
    club = db.engine.execute("SELECT * FROM clubs WHERE name LIKE '%"+ search_value + "%';")
    n = 2
    return club, n