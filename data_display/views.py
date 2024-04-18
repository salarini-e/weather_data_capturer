import csv
from datetime import date
from datetime import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from data_scraper.models import WeatherData, DataSource

# Create your views here.
def index(request):
    return render(request, 'index.html')


def fontes(request):
    context = {
        'fontes': DataSource.objects.all()
    }
    return render(request, 'fontes.html', context)


@csrf_exempt
def export_weather_data(request):
    if request.method == 'POST':
        # Recupere as datas do formulário POST
        start_date_str = request.POST.get('startdate')
        end_date_str = request.POST.get('enddate')
        fonte = request.POST.get('fonte')

        # Converta as strings de data para objetos datetime
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        print(fonte)
        # Consulte o banco de dados para recuperar os dados dentro do intervalo de tempo especificado
        weather_data = WeatherData.objects.filter(date__range=(start_date, end_date), fonte=fonte)

        # Crie a resposta CSV
        # Get the current date
        today = date.today()
        current_date = today.strftime("%Y-%m-%d")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="f{fonte}_{current_date}_weather_data.csv"'

        # Escreva os dados no arquivo CSV
        writer = csv.writer(response)
        writer.writerow(['Date', 'Temperature', 'Wind_Gust_Direction', 'Wind_Gust', 'Dewpoint', 'Precip_Rate', 'Pressure', 'Humidity', 'Precip_Accum', 'UV', 'Fonte'])
        for data in weather_data:
            writer.writerow([
                data.date.strftime('%Y-%m-%d %H:%M:%S'),
                data.temperature,
                data.wind_gust_direction,
                data.wind_gust,
                data.dewpoint,
                data.precip_rate,
                data.pressure,
                data.humidity,
                data.precip_accum,
                data.uv,
                data.fonte
            ])

        return response

    return render(request, 'filter.html', context={'fontes': WeatherData.FONTE_CHOICES})


@csrf_exempt
def view_weather_data(request):
    context={'fontes': WeatherData.FONTE_CHOICES}
    if request.method == 'POST':
        start_date_str = request.POST.get('startdate')
        end_date_str = request.POST.get('enddate')
        fonte = request.POST.get('fonte')

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        weather_data = WeatherData.objects.filter(date__range=(start_date, end_date), fonte=fonte)
        context['startdate'] = start_date_str
        context['enddate'] = end_date_str
        context['datas'] = weather_data
        return render(request, 'ver_dados.html', context)

    return render(request, 'filter_online.html', context)


def json_fontes(request):
    fontes = DataSource.objects.all()
    return JsonResponse(json.loads(serialize('json', fontes)), safe=False)

def json_dados(request,  fonte_id, dt_start, dt_end):
        dados = WeatherData.objects.filter(date__range=(dt_start, dt_end), fonte=fonte_id)
        valores = []
        for dado in dados:
            valores.append({
                'temperature': dado.temperature,
                'wind_gust_direction': dado.wind_gust_direction,
                'wind_gust': dado.wind_gust,
                'dewpoint': dado.dewpoint,
                'precip_rate': dado.precip_rate,
                'pressure': dado.pressure,
                'humidity': dado.humidity,
                'precip_accum': dado.precip_accum,
                'uv': dado.uv,
                'date': dado.date,
                'fonte': dado.fonte

            })
        return JsonResponse(valores, safe=False)