from django.http import HttpResponse
from django.shortcuts import render
import thulac

import sys
import json
from . models import Neo4j

choice = ["查询番剧","查询角色","查询公司","查询声优"]

def index(request):
    if (request.GET):
        user_sel = request.GET['user_sel']
        entity = request.GET['user_text']
        entityRelation = []

        key = choice.index(user_sel)
        if(key == 0):
            entityRelation = searchAnime(entity)
        elif(key == 1):
            entityRelation = searchRole(entity)
        elif(key == 2):
            entityRelation = searchAuthor(entity)
        elif(key == 3):
            entityRelation = searchSeiyuu(entity)
        else:
            print("wrong")

        if entityRelation:
            return render(request, 'detail.html', {'entityRelation': json.dumps(entityRelation, ensure_ascii=False)})

    return render(request, 'detail.html')

def searchAnime(entity):
    db = Neo4j()
    db.connectDB()
    anime = db.name2anime(entity)
    role = []
    seiyuu = []

    if len(anime) == 0:
        entityRelation = []
        return entityRelation
    else:
        author = db.anime2author(entity)
        classify = db.anime2classify(entity)
        platform = db.anime2platform(entity)
        entityRelation = [anime, author, classify, platform, role, seiyuu]
        return entityRelation

def searchRole(entity):
    db = Neo4j()
    db.connectDB()
    role = db.name2role(entity)
    author = []
    classify = []
    platform = []

    if len(role) == 0:
        entityRelation = []
        return entityRelation
    else:
        anime = db.role2anime(entity)
        seiyuu = db.role2seiyuu(entity)
        entityRelation = [anime, author, classify, platform, role, seiyuu]
        return entityRelation

def searchAuthor(entity):
    db = Neo4j()
    db.connectDB()
    author = db.name2author(entity)
    seiyuu = []
    classify = []
    platform = []
    role = []

    if len(author) == 0:
        entityRelation = []
        return entityRelation
    else:
        anime = db.author2anime(entity)
        entityRelation = [anime, author, classify, platform, role, seiyuu]
        return entityRelation

def searchSeiyuu(entity):
    db = Neo4j()
    db.connectDB()
    seiyuu = db.name2seiyuu(entity)
    author = []
    classify = []
    platform = []
    anime = []

    if len(seiyuu) == 0:
        entityRelation = []
        return entityRelation
    else:
        role = db.seiyuu2role(entity)
        entityRelation = [anime, author, classify, platform, role, seiyuu]
        return entityRelation