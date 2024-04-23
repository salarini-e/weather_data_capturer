from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def std_chrome_opts():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1200")
    return opts


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
