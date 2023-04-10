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

        role = db.name2role(entity)
        seiyuu = db.role2seiyuu(entity)
        anime = db.role2anime(entity)

        entityRelation = [role,anime,seiyuu]
        return render(request, 'conrole.html', {'entityRelation': json.dumps(entityRelation, ensure_ascii=False)})

    return render(request,'conrole.html')

