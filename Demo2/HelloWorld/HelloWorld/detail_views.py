from django.http import HttpResponse
from django.shortcuts import render
import thulac

import sys
import json
from . models import Neo4j

def index(request):
    return render(request, 'test.html')

def searchDetail(request):
    if (request.GET):
        entity = request.GET['user_text']
        db = Neo4j()
        db.connectDB()

        game = db.name2game(entity)

        if len(game) == 0:
            ctx = {'title': 'ctx'}
            return render(request, 'detail.html', {'ctx': json.dumps(ctx, ensure_ascii=False)})
        else:
            author = db.game2author(entity)
            classify = db.game2classify(entity)
            label = db.game2label(entity)
            entityRelation = [game, author, classify, label]

            return render(request, 'detail.html', {'entityRelation': json.dumps(entityRelation, ensure_ascii=False)})
    return render(request, 'detail.html')