from django.db import models

class DataSource(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name
    
class StationSuggestion(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovada'),
        ('rejected', 'Rejeitada'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Nome da Estação')
    url = models.URLField(verbose_name='URL da Estação')
    message = models.TextField(blank=True, null=True, verbose_name='Observações/Mensagem')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
    
    class Meta:
        verbose_name = 'Sugestão de Estação'
        verbose_name_plural = 'Sugestões de Estações'
        ordering = ['-created_at']
    
class WeatherData(models.Model):
    temperature = models.CharField(max_length=10)
    wind_gust_direction = models.CharField(max_length=20)
    wind_gust = models.CharField(max_length=20)
    dewpoint = models.CharField(max_length=10)
    precip_rate = models.CharField(max_length=10)
    pressure = models.CharField(max_length=10)
    humidity = models.CharField(max_length=10)
    precip_accum = models.CharField(max_length=10)
    uv = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)
    fonte = models.ForeignKey(DataSource, on_delete=models.CASCADE, verbose_name='Fonte/Estação')

    def __str__(self):
        return f"Estação: {self.fonte.name}, Data: {self.date.strftime('%Y-%m-%d %H:%M')}, Temperatura: {self.temperature}°C"