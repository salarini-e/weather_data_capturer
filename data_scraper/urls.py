from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [    
    path('get_dados/', views.get_dados, name='get_dados'),     
]
