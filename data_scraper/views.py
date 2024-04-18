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

from .models import WeatherData, DataSource


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

def get_dados(request):
    FONTES = DataSource.objects.all()
    wds = []
    for i in FONTES:
        url = i.url
        fonte = i.id
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(url)
            WebDriverWait(driver, 100)
            wd = find_dados_via_webdriver(driver)
            wd["fonte"] = fonte
            WeatherData.objects.create(**wd)
            wds.append(wd)
        except Exception as ex:
            logging.warning("Can't fetch", ex, url)
        finally:
            driver.quit()
    return HttpResponse(json.dumps(wds), content_type="application/json")

def create_demo_sources(request):
    if DataSource.objects.all().exists():
        return HttpResponse("OK. DEMO SOURCES ALREADY CREATED")
    
    DataSource.objects.create(name="Pico do Caledônia", url="https://www.wunderground.com/dashboard/pws/IRIOGRAN2")
    DataSource.objects.create(name="Stucky", url="https://www.wunderground.com/dashboard/pws/IRIOGRAN3")
    DataSource.objects.create(name="Barão (Jardim Califórnia)", url="https://www.wunderground.com/dashboard/pws/IRIOGRAN4")
    DataSource.objects.create(name="Edifício Itália (Centro)", url="https://www.wunderground.com/dashboard/pws/IRIOGRAN5")
    return HttpResponse("OK. DEMO SOURCES CREATED")