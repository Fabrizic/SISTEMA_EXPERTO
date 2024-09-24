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

# Espera hasta que los elementos de las películas estén visibles
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'movies-list--large-item'))
)

# Intentar cerrar el pop-up de consentimiento
try:
    consent_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'consent--container--content--buttons'))
    )
    consent_button.click()
    print("Pop-up de consentimiento cerrado.")
except Exception as e:
    print("No se pudo cerrar el pop-up de consentimiento:", e)

# Intentar cargar más películas haciendo clic en el botón "Ver más películas" con JavaScript
try:
    ver_mas_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'movies-list--view-more-button'))
    )
    
    # Desplazarse hacia el botón
    driver.execute_script("arguments[0].scrollIntoView(true);", ver_mas_button)
    
    # Hacer clic con JavaScript para evitar cualquier bloqueo por otros elementos
    driver.execute_script("arguments[0].click();", ver_mas_button)
    
    # Esperar unos segundos para permitir que las películas adicionales se carguen
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'movies-list--large-item'))
    )
    print("Clic en 'Ver más películas' exitoso.")
except Exception as e:
    print("No se pudo hacer clic en el botón 'Ver más películas':", e)

# Obtener el HTML de la página ya renderizada
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Encuentra todos los elementos de películas en la página
movies = soup.find_all('div', class_='movies-list--large-item')

# Lista para almacenar los datos de las películas
peliculas_data = []

# Verifica si encontró películas
if not movies:
    print("No se encontraron películas.")
else:
    for movie in movies:
        title_tag = movie.find('h2', class_='movies-list--large-movie-description-title')
        title = title_tag.text.strip() if title_tag else 'Título no disponible'
        
        extra_info_tag = movie.find('h3', class_='movies-list--large-movie-description-extra')
        extra_info = extra_info_tag.text.strip() if extra_info_tag else 'Información extra no disponible'
        
        peliculas_data.append({
            'titulo': title,
            'descripcion': extra_info
        })

with open('peliculas_cineplanet.json', 'w', encoding='utf-8') as f:
    json.dump(peliculas_data, f, ensure_ascii=False, indent=4)

# Cierra el navegador después de completar el scraping
driver.quit()
