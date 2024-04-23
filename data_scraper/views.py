import json
import logging

from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

import data_scraper.scra as scra
from .models import WeatherData, DataSource


def get_dados(request):
    FONTES = DataSource.objects.all()
    wds = []
    for i in FONTES:
        url = i.url
        fonte = i.id
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=scra.std_chrome_opts())
        try:
            driver.get(url)
            WebDriverWait(driver, 100)
            wd = scra.find_dados_via_webdriver(driver)
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