from django.contrib import admin
from .models import WeatherData, DataSource, StationSuggestion

@admin.register(StationSuggestion)
class StationSuggestionAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'url']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'url', 'message', 'status')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['date', 'fonte', 'temperature', 'humidity', 'pressure']
    list_filter = ['fonte', 'date']
    search_fields = ['fonte__name']
    date_hierarchy = 'date'
    
    fieldsets = (
        (None, {
            'fields': ('fonte', 'date')
        }),
        ('Dados Meteorológicos', {
            'fields': ('temperature', 'humidity', 'pressure', 'wind_gust', 'wind_gust_direction', 'dewpoint', 'precip_rate', 'precip_accum', 'uv')
        }),
    )

@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    search_fields = ['name']