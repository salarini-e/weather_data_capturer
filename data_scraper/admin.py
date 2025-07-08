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

admin.site.register(WeatherData)
admin.site.register(DataSource)