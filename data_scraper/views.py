from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
from django.http import JsonResponse
from .models import WeatherData
import csv
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from datetime import date

def index(request):
    return render(request, 'index.html')

def fontes(request):
    return render(request, 'fontes.html')

def verificar_status(request):
    FONTES =[   
                ('1', "https://www.wunderground.com/dashboard/pws/INOVAF18"),
                ('2', "https://www.wunderground.com/dashboard/pws/INOVAF19"),
                ('3', "https://www.wunderground.com/dashboard/pws/INOVAF27"),
                ('4', "https://www.wunderground.com/dashboard/pws/INOVAF26")
            ]
    
    for i in FONTES:
        url = i[1]
    
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get(url)
        WebDriverWait(driver, 100)    
        dados_ = []
        try:        
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            dashboard_content = soup.find('div', class_='dashboard__module__content')
            value_element = dashboard_content.find_all('span', class_='wu-value')
            for value in value_element:
                dados_.append(value.text)

            dados = {
                'temperature': dados_[0],
                'wind_gust_direction': dados_[2],
                'wind_gust': dados_[3],
                'dewpoint': dados_[4],
                'precip_rate': dados_[5],
                'pressure': dados_[6],
                'humidity': dados_[7],
                'precip_accum': dados_[8],
                'uv': dados_[9],
                'fonte': i[0]
            }

            weather_data = WeatherData.objects.create(**dados)        
            # soup = BeautifulSoup(driver.page_source, 'html.parser')

            # dashboard_content = soup.find('div', class_='dashboard__module__content')
            # value_element = dashboard_content.find('span', class_='wu-value')
            # dados['temperatura'] = value_element.text   
            # wind_gust = soup.find('div', class_='weather__data weather__wind-gust')
            # wind_gust_text = wind_gust.find('div', class_='weather__text')
            # dados['vento_rajada'] =  []
            # values = wind_gust_text.find_all('span', class_='wu-value')
            # dados['vento_rajada'].append(values[0].text)
            # dados['vento_rajada'].append(values[1].text)
        except Exception as e:
            print(e)
            dados = {
                'temperature': 'null',
                'wind_gust_direction': 'null',
                'wind_gust': 'null',
                'dewpoint': 'null',
                'precip_rate': 'null',
                'pressure': 'null',
                'humidity': 'null',
                'precip_accum': 'null',
                'uv': 'null',
                'fonte': i[0]
            }

            weather_data = WeatherData.objects.create(**dados)  
        finally:
            driver.quit()
    return HttpResponse(json.dumps(dados), content_type="application/json")
    
def dados(request):
        dados = WeatherData.objects.all()
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