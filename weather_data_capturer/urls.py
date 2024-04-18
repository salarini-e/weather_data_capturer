from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('data_scraper.urls')),
    path('', include('data_display.urls')),
]
