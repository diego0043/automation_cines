import re
import time
import openpyxl
import datetime
from config_selenium import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def scrape_movie_details(movie_listing):
    """
    Extrae los detalles de una película desde un elemento de la lista de proyecciones.

    Args:
        movie_listing (WebElement): Elemento de la lista de proyecciones de la película.

    Returns:
        tuple: Título de la película y un diccionario con los formatos y horarios.
    """
	# Encuentra el título de la película
    movie_title_element = movie_listing.find_element(By.CSS_SELECTOR, ".movie-projection__inner h2")
    movie_title = movie_title_element.text
    presence=False

    # Encuentra y haz clic en el enlace "Ver todos" si está presente
    try:
        see_all_link = movie_listing.find_element(By.CSS_SELECTOR, "li.link-see-all a")
        see_all_link.click()
        presence=True
        time.sleep(2)  # Espera un momento para que la página cargue los horarios adicionales

        # Busca los elementos después de hacer clic en "Ver todos"
        movie_listing = driver.find_element(By.CSS_SELECTOR, ".movie-projection")
    except NoSuchElementException:
        presence=False
        pass

    # Encuentra los formatos y horarios
    format_times_dict = {}
    
    # Procesar los formatos definidos por h3.title-attribute y sus correspondientes ul
    format_headers = movie_listing.find_elements(By.CSS_SELECTOR, "h3.title-attribute")
    for format_header in format_headers:
        language_full = format_header.text.strip()
        
        # Dividir el formato en tipo (2D/3D) e idioma (Subtitulado/Doblado)
        format_parts = language_full.split()
        format_type = next((part for part in format_parts if part in ['2D', '3D']), 'No especificado')
        language = next((part for part in format_parts if part in ['SUBTITLE', 'DUB']), 'No especificado')
        
        ul_element = format_header.find_element(By.XPATH, "following-sibling::ul[1]")
        time_elements = ul_element.find_elements(By.CSS_SELECTOR, "li")
        
        for time_element in time_elements:
            schedule_times = time_element.find_element(By.CSS_SELECTOR, "label").text.strip()
            
            if language not in format_times_dict:
                format_times_dict[language] = []
            format_times_dict[language].append((schedule_times, format_type))

    # Procesar los formatos definidos por ul li:not(.link-see-all)
    time_elements = movie_listing.find_elements(By.CSS_SELECTOR, "ul li:not(.link-see-all)")

    for time_element in time_elements:
        # Extraer la hora
        label_element = time_element.find_element(By.CSS_SELECTOR, "label")
        label_text = label_element.text.split("\n")

        if label_text:
            schedule_times = label_text[0].strip()
        else:
            continue

        # Extraer el formato
        try:
            span_element = time_element.find_element(By.CSS_SELECTOR, "span")
            format_info_element = span_element.get_attribute("title").strip()
            format_parts = format_info_element.split(", ")

            format_type = None
            language = None

            for part in format_parts:
                if '3D' in part:
                    format_type = '3D'
                elif '2D' in part:
                    format_type = '2D'
                elif part in ['SUBTITLE', 'DUB']:
                    language = part

            if not language:
                language = "No especificado"

            # Actualizar el diccionario con la hora y el tipo de formato
            if language not in format_times_dict:
                format_times_dict[language] = []
            format_times_dict[language].append((schedule_times, format_type))

        except NoSuchElementException:
            continue
	
	# Verifica la opcionn ver todos y si esta al finalizar regresa a la pagina anterior
    if presence:
        driver.back() 

    return movie_title, format_times_dict

# Obtener la fecha actual
current_date_ = datetime.date.today().strftime('%d-%m-%Y')
url ="https://cinepolis.com.hn/"

# Navegar a la página web
driver.get(url)
driver.implicitly_wait(5)
close_popup('.welcome-video-popup .button-close')

# Seleccionar cine
try:
	button_element=driver.find_element(By.CSS_SELECTOR,'a.show-cinemas-popup')
	button_element.click()
except:
	print("No se pudo seleccionar un cine")

# Obtener los enlaces de las opciones de cine
options_links = [option.get_attribute('href') for option in driver.find_elements(By.CSS_SELECTOR, '.cinemas .Cinema_cinema__3_YUn a')]

# Procesar cada enlace de cine
for option_link in options_links:
	driver.get(option_link)

	main_element = driver.find_element(By.CSS_SELECTOR, '.main__inner')
	cinema_element=main_element.find_element(By.CSS_SELECTOR,'.reservation-step')
	cinema_name = cinema_element.find_element(By.TAG_NAME, "h3").text
	cinema_name_parts = cinema_name.split(": ")[1].split(" ")
	cinema_brand = cinema_name_parts[0].capitalize()
	cinema_location = " ".join(cinema_name_parts[1:]).title()

	movie_projections_section = main_element.find_element(By.CSS_SELECTOR, ".movie-projections")

	# Obtener los elementos de las películas
	movie_items = movie_projections_section.find_elements(By.CSS_SELECTOR, ".movie-projection-alt")
	for movie_listing in movie_items:
		movie_title, format_times_dict  = scrape_movie_details(movie_listing)

		# Escribir los datos de las películas en la hoja de Excel
		for language, times_with_type in format_times_dict.items():
			for schedule_times, format_type in times_with_type:
				write_movie_data(sheet, current_date_, 'Honduras', cinema_brand, cinema_location, movie_title, schedule_times, format_type, language)
	
	# Vuelve a la selección de cines
	try:
		button_element=driver.find_element(By.CSS_SELECTOR,'a.show-cinemas-popup')
		button_element.click()
	except:
		print("No se pudo seleccionar un cine")

# Guardar el libro de trabajo de Excel
current_hour = datetime.datetime.now().strftime('%H-%M-%S')
distin_name = "results/cinepolis-"+str(current_date_) + \
	" "+str(current_hour)+".xlsx"
workbook.save(filename=distin_name)
print("Información de los cines guardada en el archivo Excel.")

# Salir del controlador
driver.quit()