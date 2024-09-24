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
options = webdriver.ChromeOptions()
# No usar el modo headless para poder resolver el CAPTCHA manualmente
# options.add_argument('--headless')  # Ejecutar en modo headless (sin interfaz gráfica)
options.add_argument('--disable-gpu')  # Desactivar la aceleración de hardware
options.add_argument('--no-sandbox')  # Añadir esta opción para evitar problemas de sandboxing
options.add_argument('--disable-dev-shm-usage')  # Añadir esta opción para evitar problemas de memoria compartida

driver = webdriver.Chrome(service=service, options=options)

# URL de la página de Cinemark
url = 'https://www.cinemark-peru.com/peliculas'
driver.get(url)

# Espera hasta que los elementos de las películas estén visibles
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'hover-content'))
)

# Obtener el HTML de la página ya renderizada
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Encuentra todos los elementos de películas en la página
movies = soup.find_all('a', class_='hover-content')

# Lista para almacenar los datos de las películas
peliculas_data = []

# Verifica si encontró películas
if not movies:
    print("No se encontraron películas.")
else:
    for movie in movies:
        # Extraer el título de la película y convertirlo a minúsculas
        title_tag = movie.find('div', class_='movie-title')
        title = title_tag.text.strip() if title_tag else 'Titulo no disponible'
        
        # Extraer la información extra (duración y clasificación) y formatearla
        info_tag = movie.find('div', class_='movie-info')
        if info_tag:
            info_items = [item.strip() for item in info_tag.stripped_strings]
            extra_info = ', '.join(info_items)
        else:
            extra_info = 'Información extra no disponible'
        
        # Agregar los datos de la película a la lista
        peliculas_data.append({
            'titulo': title,
            'descripcion': extra_info
        })

# Guardar los datos en un archivo JSON
with open('peliculas_cinemark.json', 'w', encoding='utf-8') as f:
    json.dump(peliculas_data, f, ensure_ascii=False, indent=4)

# Cierra el navegador después de completar el scraping
driver.quit()