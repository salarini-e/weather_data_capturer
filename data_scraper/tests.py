import os

from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

import data_scraper.scra as scra


class FindTestCase(TestCase):
    def setUp(self):
        # Animal.objects.create(name="lion", sound="roar")
        pass

    def test_find_dados_via_webdriver(self):
        driver = webdriver.Chrome(options=scra.std_chrome_opts())
        try:
            driver.set_network_conditions(offline=True, latency=10000, throughput=0)
            driver.get(f"file://{os.path.abspath('snapshots/data_capture_01.html')}")
            WebDriverWait(driver, 100)
            dados = scra.find_dados_via_webdriver(driver)
        finally:
            driver.close()
        self.assertEqual(
            dados,
            {
                'temperature': '56.3',
                'wind_gust_direction': '0.0',
                'wind_gust': '0.0',
                'dewpoint': '55.8',
                'precip_rate': '0.00',
                'pressure': '26.88',
                'humidity': '98',
                'precip_accum': '0.00',
                'uv': '0'}
        )
