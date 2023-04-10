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
        entityRelation = []
        entity = request.GET['user_text']

        if(len(entity)!=0):
            ner = NER()
            entityRelation = ner.question_answering(entity)

        if entityRelation:
            return render(request, 'search.html', {'entityRelation': json.dumps(entityRelation, ensure_ascii=False)})

    return render(request,'search.html')

