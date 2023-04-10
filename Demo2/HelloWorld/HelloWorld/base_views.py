from django.shortcuts import render
from django.views.decorators import csrf

# Create your views here.
def index(request):
    return render(request,'base.html')