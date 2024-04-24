import sys

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

import data_scraper.scra as scra


def main(argv):
    driver = webdriver.Chrome(options=scra.std_chrome_opts())
    try:
        driver.get("https://www.wunderground.com/dashboard/pws/INOVAF19")
        WebDriverWait(driver, 100)
        print("<!DOCTYPE html>")
        print(driver.page_source)
    finally:
        driver.close()
    pass


# run with:
# python -m data_display.cli > snapshots/data_capture_01.html
if __name__ == "__main__":
    main(sys.argv)
