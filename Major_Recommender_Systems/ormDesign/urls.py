#coding=utf-8

#coding=utf-8

from django.urls import path
from . import views

urlpatterns = [
    path('1/', views.getCategory, name='getCategory'),
    path('2/', views.getProvinces, name='getProvinces'),
    path('3/', views.getColleges, name='getColleges'),
    path('4/', views.getRankings, name='getRankings'),
    path('5/', views.getAreas, name='getAreas'),
    path('6/', views.getMajors, name='getMajors'),
]