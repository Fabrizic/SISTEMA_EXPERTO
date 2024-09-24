import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Path al driver de Chrome (asegúrate de tener la ruta correcta)
chrome_driver_path = r"C:\Users\LG\Downloads\chromedriver-win64\chromedriver.exe"

# Configura Selenium para usar Chrome
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# URL de la página de Cineplanet
url = 'https://www.cineplanet.com.pe/peliculas'
driver.get(url)