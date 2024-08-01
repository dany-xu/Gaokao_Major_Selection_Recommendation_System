#coding=utf-8

from django.urls import path
from . import views
import recommender
urlpatterns = [
    path('', views.index, name='index'),
    path('map_test/', views.map, name='map'),
    path('college_info/', views.college_info, name='college_info'),
    path('major_info/', views.major_info, name='major_info'),
    path('psychological_test/', views.psychological_test, name='psychological_test'),
    #path('test_final/', views.test, name='test'),
    #path('test_final/recommender/result/',recommender.views.predict,name='test')
]