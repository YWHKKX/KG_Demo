from django.http import HttpResponse
from django.shortcuts import render
import thulac

import sys
import json
from . models import Neo4j

def index(request):
    db = Neo4j()
    db.connectDB()
    ctx = db.get_all_anime()

    return render(request, 'catalog.html', {'ctx': json.dumps(ctx, ensure_ascii=False)})

