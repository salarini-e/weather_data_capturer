from django.contrib import admin
from .models import WeatherData, DataSource

admin.site.register(WeatherData)
admin.site.register(DataSource)