from django.db import migrations, transaction

def migrate_fonte_data(apps, schema_editor):
    """Migra os dados da coluna fonte (1, 2, 3, 4) para DataSource correspondentes"""
    WeatherData = apps.get_model('data_scraper', 'WeatherData')
    DataSource = apps.get_model('data_scraper', 'DataSource')
    
    # Certifique-se de que existem as fontes de dados no sistema
    data_sources = {}
    
    # Mapeamento de IDs antigos para novos
    fonte_mapping = {
        "1": ["Pico do Caledônia", 'https://www.wunderground.com/dashboard/pws/INOVAF18 '],
        "2": ["Stucky", 'https://www.wunderground.com/dashboard/pws/INOVAF19'],
        "3": ["Barão (Jardim Califórnia)", 'https://www.wunderground.com/dashboard/pws/INOVAF27'],
        "4": ["Edifício Itália (Centro)", 'https://www.wunderground.com/dashboard/pws/INOVAF26']
    }
    
    # Cria DataSources se não existirem
    for fonte_id, data in fonte_mapping.items():
        name = data[0]
        url = data[1]
        data_source, created = DataSource.objects.get_or_create(
            name=name,
            defaults={'url': url}
        )
        data_sources[fonte_id] = data_source
    
    # Atualiza cada registro de WeatherData
    with transaction.atomic():
        for data in WeatherData.objects.all():
            fonte_id = data.fonte
            if fonte_id and fonte_id in data_sources:
                data.fonte = data_sources[fonte_id]
                data.save()
            else:
                # Se não encontrar uma fonte correspondente, use a primeira disponível
                if data_sources:
                    data.fonte = list(data_sources.values())[0]
                    data.save()

class Migration(migrations.Migration):

    dependencies = [
        ('data_scraper', '0005_alter_weatherdata_fonte'),
    ]

    operations = [
        migrations.RunPython(migrate_fonte_data),
    ]
