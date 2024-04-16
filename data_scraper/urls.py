from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_dados/', views.verificar_status, name='verificar_status'),
    path('fontes/', views.fontes, name='fontes'),
    path('dados/', views.dados, name='dados'),
    path('download/', views.export_weather_data, name='download'),
    path('ver-dados/', views.view_weather_data, name='ver_dados'),
]
