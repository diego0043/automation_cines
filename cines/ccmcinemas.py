from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup

# Ruta al ejecutable de EdgeDriver
path = 'C:/Users/ve180/Downloads/edgedriver_win64/msedgedriver.exe'

# Configurar las opciones de Edge
options = Options()
# Esta opción mantiene la pestaña abierta después de que el script termine
options.detach = True

# Configurar el servicio de EdgeDriver
service = Service(executable_path=path)

# Crear el driver de Edge con las opciones y el servicio configurados
driver = webdriver.Edge(service=service, options=options)

# Abrir la página web
driver.get('https://ccmcinemas.com/')

# Maximizar la ventana del navegador (opcional)
driver.maximize_window()

# Esperar unos segundos para asegurarse de que la página se cargue completamente (opcional)
time.sleep(2)

# Encontrar todos los elementos <a> que contienen enlaces a diferentes cines
links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/cines/"]')
cartelera = ""
fecha = date.today()


def close_popup():
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.spu-close')))

        # Cerrar el cuadro de diálogo emergente
        close_button = driver.find_element(By.CSS_SELECTOR, '.spu-close')
        close_button.click()
    except Exception as e:
        print(f"No hay pop-up para cerrar")


def return_home():
    driver.get('https://ccmcinemas.com/')


# Iterar sobre los elementos encontrados
for i in range(len(links)):
    # Volver a encontrar los elementos <a> después de cada iteración para evitar StaleElementReferenceException
    links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/cines/"]')

    # Obtener el URL del cine
    cine_url = links[i].get_attribute('href')

    # Imprimir información (opcional)
    print(f"URL del cine: {cine_url}")

    # Navegar a la URL del cine
    driver.get(cine_url)

    # Esperar a que la página se cargue completamente
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body')))

    try:
        close_popup()

        cartelera = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "CARTELERA")]')))
        cartelera.click()

        # Esperar a que la página de la cartelera se cargue completamente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Encontrar todos los botones con la clase especificada
        botones = driver.find_elements(
            By.CSS_SELECTOR, 'a._self.pt-cv-readmore.btn.btn-success')

        # Tomar nombre de las pelis antes de hacer clic
        titulos = driver.find_elements(By.CSS_SELECTOR, 'h6.pt-cv-title')

        # Hacer clic en cada botón utilizando índices
        for j in range(len(botones)):
            try:
                # Volver a encontrar los botones después de cada interacción
                botones = driver.find_elements(
                    By.CSS_SELECTOR, 'a._self.pt-cv-readmore.btn.btn-success')
                boton = botones[j]

                # volver a obtener titulos
                titulos = driver.find_elements(
                    By.CSS_SELECTOR, 'h6.pt-cv-title')
                titulo = titulos[j].text
                print(f"Titulo: {titulo}")
                print(f"Fecha: {fecha}")

                boton.click()

                # Esperar a que la página se cargue completamente (ajustar según necesidad)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body')))

                try:
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    # Encontrar el elemento que contiene la información deseada
                    info = soup.find_all(
                        'span', class_='ListatandasCalendario')

                    print(info)
                except Exception as e:
                    print(f"Error al extraer la información: {e}")

                # Volver a la página de la cartelera
                driver.back()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body')))
            except Exception as e:
                print(f"Error al hacer clic en el botón: {e}")

        # Volver a la página inicial
        return_home()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))
    except Exception as e:
        print(f"Error: {e}")
