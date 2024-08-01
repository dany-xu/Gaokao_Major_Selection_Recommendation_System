#coding=utf-8

from django.urls import path
from . import views

urlpatterns = [
    path('1', views.predict1, name='prediction'),
    path('2', views.predict2, name='prediction'),
    path('', views.predict, name='prediction'),
]