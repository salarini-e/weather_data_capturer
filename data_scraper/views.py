import csv
import json
from datetime import date
from datetime import datetime
import logging

from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.serializers import serialize
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .models import WeatherData


def index(request):
    return render(request, 'index.html')


def fontes(request):
    return render(request, 'fontes.html')


def find_dados_via_bs(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    dashboard_content = soup.find('div', class_='dashboard__module__content')
    value_element = dashboard_content.find_all('span', class_='wu-value')
    dados_ = []
    for value in value_element:
        dados_.append(value.text)
    return {
        'temperature': dados_[0],
        'wind_gust_direction': dados_[2],
        'wind_gust': dados_[3],
        'dewpoint': dados_[4],
        'precip_rate': dados_[5],
        'pressure': dados_[6],
        'humidity': dados_[7],
        'precip_accum': dados_[8],
        'uv': dados_[9]
    }


def find_dados_via_webdriver(driver):
    return {
        k: element.text for k, element in zip(
            ["temperature", None, "wind_gust_direction", "wind_gust", "dewpoint", "precip_rate", "pressure", "humidity",
             "precip_accum", "uv"],
            driver.find_elements(By.CSS_SELECTOR, "div.dashboard__module__content span.wu-value")
        )
        if k
    }


def verificar_status(request):
    FONTES = [
                ('1', "https://www.wunderground.com/dashboard/pws/INOVAF18"),
                ('2', "https://www.wunderground.com/dashboard/pws/INOVAF19"),
                ('3', "https://www.wunderground.com/dashboard/pws/INOVAF27"),
                ('4', "https://www.wunderground.com/dashboard/pws/INOVAF26")
            ]
    wds = []
    for i in FONTES:
        url = i[1]
        fonte = i[0]

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(url)
            WebDriverWait(driver, 100)
            # wds = find_dados_via_bs(wds)
            # wds["fonte"] = fonte
            wd = find_dados_via_webdriver(driver)
            wd["fonte"] = fonte
            WeatherData.objects.create(**wd)
            wds.append(wd)
        except Exception as ex:
            logging.warning("Can't fetch", ex, url)
        finally:
            driver.quit()
    return HttpResponse(json.dumps(wds), content_type="application/json")


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
