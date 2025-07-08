from django.db import migrations, transaction

def update_datasource_urls(apps, schema_editor):
    """Atualiza as URLs das fontes de dados"""
    DataSource = apps.get_model('data_scraper', 'DataSource')
    
    # Mapeamento de nomes para URLs corretas
    url_mapping = {
        "Pico do Caledônia": 'https://www.wunderground.com/dashboard/pws/INOVAF18',
        "Stucky": 'https://www.wunderground.com/dashboard/pws/INOVAF19',
        "Barão (Jardim Califórnia)": 'https://www.wunderground.com/dashboard/pws/INOVAF27',
        "Edifício Itália (Centro)": 'https://www.wunderground.com/dashboard/pws/INOVAF26'
    }
    
    # Atualiza cada DataSource com a URL correta
    with transaction.atomic():
        for name, url in url_mapping.items():
            try:
                data_source = DataSource.objects.get(name=name)
                data_source.url = url
                data_source.save()
            except DataSource.DoesNotExist:
                # Cria se não existir
                DataSource.objects.create(name=name, url=url)

class Migration(migrations.Migration):

    dependencies = [
        ('data_scraper', '0006_migrate_fontes_data'),
    ]

    operations = [
        migrations.RunPython(update_datasource_urls),
    ]
