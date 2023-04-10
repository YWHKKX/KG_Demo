from django.http import HttpResponse
from django.shortcuts import render
import thulac

import sys
import json
from . models import Neo4j
from paddlenlp import Taskflow
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

from . NER import NER

def index(request):
    if (request.GET):
        entity = request.GET['user_text']
        db = Neo4j()
        db.connectDB()

        anime = db.name2anime(entity)
        role = db.anime2role(entity)
        platform = db.anime2platform(entity)
        classify = db.anime2classify(entity)
        author = db.anime2author(entity)
        entityRelation = [anime,role,platform,classify,author]

        return render(request, 'context.html', {'entityRelation': json.dumps(entityRelation, ensure_ascii=False)})

    return render(request,'context.html')

