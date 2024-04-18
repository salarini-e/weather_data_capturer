from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index, name='index'),
    path('fontes/', views.fontes, name='fontes'),
    path('download/', views.export_weather_data, name='download'),
    path('ver-dados/', views.view_weather_data, name='ver_dados'),

    path('api/fontes/', views.json_fontes, name='json_fontes'), 
    path('api/dados/font=<int:fonte_id>/start=<dt_start>/end=<dt_end>/', views.json_dados, name='json_dados'),
]