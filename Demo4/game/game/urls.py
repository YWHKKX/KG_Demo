"""game URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path as url
from . import base_views
from . import detail_views
from . import search_views
from . import catalog_views
from . import context_views
from . import conrole_views

urlpatterns = [
    url(r'^$', base_views.index),
    url(r'^detail', detail_views.index),
    url(r'^search', search_views.index),
    url(r'^catalog', catalog_views.index),
    url(r'^context', context_views.index),
    url(r'^conrole', conrole_views.index)
]