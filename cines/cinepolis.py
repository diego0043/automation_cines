import re
import openpyxl
import datetime
import time as tm
from config_selenium import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def scrape_movie_details(movie_listing):
    """
    Extrae los detalles de una película de un elemento de la lista de películas.

    Args:
        movie_listing (WebElement): Elemento de la lista que contiene información de la película.

    Returns:
        tuple: Título de la película y un diccionario con formatos y sus horarios.
    """
    try:
        movie_title_element = movie_listing.find_element(By.CSS_SELECTOR, ".informacion-general h3")
    except NoSuchElementException:
        movie_title_element = movie_listing.find_element(By.CSS_SELECTOR, "header h3 a")

    movie_title = movie_title_element.text.strip()

    formats_with_times = {}
    try:
        format_elements = movie_listing.find_elements(By.CSS_SELECTOR, ".formatos .formato")
        if format_elements:
            for format_element in format_elements:
                formato_imagen_div = format_element.find_elements(By.CSS_SELECTOR, ".formato-imagen")
                if formato_imagen_div:
                    formato_imagen = formato_imagen_div[0].find_element(By.TAG_NAME, "img")
                    imagen_alt = formato_imagen.get_attribute("alt")
                    if '3D' in imagen_alt:
                        format_type = "3D"
                    elif 'junior' in imagen_alt:
                        format_type = "Junior"
                    else:
                        format_type = "2D"
                else:
                    format_type = "2D"

                format_name = format_element.find_element(By.CSS_SELECTOR, ".formato-nombre").text.strip()
                times = [a.text.strip() for a in format_element.find_elements(By.CSS_SELECTOR, ".horas a p")]

                if format_name in formats_with_times:
                    formats_with_times[format_name].append((times, format_type))
                else:
                    formats_with_times[format_name] = [(times, format_type)]
        else:
            raise NoSuchElementException

    except NoSuchElementException:
        format_elements = movie_listing.find_elements(By.CSS_SELECTOR, ".horarioExp")
        for format_element in format_elements:
            times = [a.text.strip() for a in format_element.find_elements(By.CSS_SELECTOR, "time a")]
            format_type = format_element.find_element(By.CSS_SELECTOR, "p span").text.strip().replace("\n", "").replace("\r", "")

            if format_type != "3D":
                format_type = "2D"

            format_name = format_element.get_attribute("class").split()[-1]

            if format_name in formats_with_times:
                formats_with_times[format_name].append((times, format_type))
            else:
                formats_with_times[format_name] = [(times, format_type)]

    return movie_title, formats_with_times

def safe_find_elements(driver, by, value, attempts=3):
    """
    Intenta encontrar elementos múltiples con múltiples intentos.

    Args:
        driver (WebDriver): El controlador de Selenium.
        by (By): El método para encontrar el elemento.
        value (str): El valor para encontrar el elemento.
        attempts (int): Número de intentos.

    Returns:
        list: Lista de elementos encontrados.
    """
    while attempts > 0:
        try:
            elements = driver.find_elements(by, value)
            return elements
        except StaleElementReferenceException:
            attempts -= 1
            tm.sleep(1)
    return []

def safe_click(element, attempts=3):
    """
    Intenta hacer clic en un elemento con múltiples intentos.

    Args:
        element (WebElement): El elemento en el que hacer clic.
        attempts (int): Número de intentos.

    Returns:
        bool: True si se hizo clic con éxito, False en caso contrario.
    """
    while attempts > 0:
        try:
            element.click()
            return True
        except (StaleElementReferenceException, ElementClickInterceptedException):
            attempts -= 1
            tm.sleep(1)
    return False

# Configuración inicial
current_date_ = datetime.date.today().strftime('%d-%m-%Y')
cinepolis_urls = [
    "https://cinepolis.com.sv/",
    "https://cinepolis.com.gt/",
    "https://cinepolis.co.cr/",
    "https://cinepolis.com.pa/",
]

try:
    for url in cinepolis_urls:
        driver.get(url)
        close_popup('#takeover-close')

        # Seleccionar ciudad
        try:
            select = Select(driver.find_element(By.ID, 'ciudad'))
        except NoSuchElementException:
            try:
                select = Select(driver.find_element(By.ID, 'cmbCiudades'))
            except NoSuchElementException:
                print("Ninguno de los IDs fue encontrado.")

        options = select.options
        driver.implicitly_wait(5)

        for i in range(len(options)):
            driver.get(url)
            close_popup('#takeover-close')
            
            try:
                # Seleccionar la opción nuevamente
                select = Select(driver.find_element(By.ID, 'ciudad'))  # Asume que el ID es 'ciudad'
            except NoSuchElementException:
                try:
                    select = Select(driver.find_element(By.ID, 'cmbCiudades'))
                except NoSuchElementException:
                    print("Ninguno de los IDs fue encontrado.")
                    continue
                
            options = select.options
            select.select_by_index(i)
            selected_option = select.first_selected_option
            location_text = selected_option.text
            country = location_text.split(', ')[-1]

            if country in ['Jutiapa', 'Zacapa', 'San Pedro Carchá']:
                country = 'Guatemala'
            elif country == 'David Chiriquí':
                country = 'Panamá'

            # Intentar encontrar y hacer clic en el botón de envío
            try:
                button_element = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            except NoSuchElementException:
                try:
                    button_element = driver.find_element(By.CSS_SELECTOR, ".btnEnviar[type='submit']")
                except NoSuchElementException:
                    print("No se pudo encontrar el botón o el input")
                    continue

            button_element.click()
            max_retries = 3
            retry_count = 0

            while retry_count < max_retries:
                try:
                    cinemas = safe_find_elements(driver, By.CSS_SELECTOR, "#listBillboards .ScheduleMovie__ScheduleMovieComponent-sc-7752wm-0")

                    if cinemas:
                        break
                    else:
                        error_element = driver.find_element(By.CSS_SELECTOR, ".error-modal .error")
                        retry_button = error_element.find_element(By.CSS_SELECTOR, "button.btn")
                    
                        if safe_click(retry_button):
                            print('Hubo un error y se recargó la página')
                            retry_count += 1
                            driver.implicitly_wait(10)  # Aumentar el tiempo de espera
                        else:
                            print("No se pudo hacer clic en el botón de reintento.")
                            raise NoSuchElementException

                except NoSuchElementException:
                    try:
                        wait = WebDriverWait(driver, 10)
                        cinemas = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".divComplejo")))

                        if cinemas:
                            break

                    except TimeoutException:
                        print("Ningún elemento fue encontrado.")
                        break

            for movie in cinemas:
                try:
                    cinema_element = movie.find_element(By.CSS_SELECTOR, "header[id^='cinema-']")
                    cinema_name = cinema_element.find_element(By.TAG_NAME, "h2").text
                    cinema_name_parts = cinema_name.split(" ")
                    cinema_brand = cinema_name_parts[0].capitalize()
                    cinema_location = " ".join(cinema_name_parts[1:]).title()
                except NoSuchElementException:
                    try:
                        cinema_element = movie.find_element(By.CSS_SELECTOR, ".divFecha")
                        cinema_name = cinema_element.find_element(By.TAG_NAME, "h2").text
                        cinema_name_parts = cinema_name.split(" ")
                        cinema_brand = cinema_name_parts[0].capitalize()
                        cinema_location = " ".join(cinema_name_parts[1:]).title().strip().replace("\n", "").replace("\r", "")
                        cinema_location = cinema_location[:-1].strip()
                    except:
                        print('No se encontró ninguna lista de películas')
                        continue

                try:
                    list_movies = movie.find_element(By.CLASS_NAME, "movies")
                    movie_elements = list_movies.find_elements(By.CSS_SELECTOR, ".SingleScheduleMovie__SingleScheduleComponent-sc-1n3hti2-0")

                    if not movie_elements:
                        raise NoSuchElementException
                except NoSuchElementException:
                    movie_elements = movie.find_elements(By.CSS_SELECTOR, "article.row.tituloPelicula")
                    
                for movie_listing in movie_elements:
                    # Extraer los detalles de la película
                    movie_title, formats_with_times = scrape_movie_details(movie_listing)

                    # Escribir los datos de la película en la hoja de Excel para cada horario
                    for format_name, times_with_type in formats_with_times.items():
                        for times, format_type in times_with_type:
                            for time in times:
                                # Escribir los datos en el Excel:
                                write_movie_data(sheet, datetime.date.today().strftime('%d-%m-%Y'), country, cinema_brand, cinema_location, movie_title, time, format_type, format_name)

finally:
    driver.quit()
    # Guardar el libro de trabajo de Excel
    current_hour = datetime.datetime.now().strftime('%H-%M-%S')
    distin_name = "results/cinepolis-"+str(current_date_) + \
        " "+str(current_hour)+".xlsx"
    workbook.save(filename=distin_name)
    print("Información de los cines guardada en el archivo Excel.")

