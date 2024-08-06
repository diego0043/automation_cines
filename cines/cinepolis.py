import re
import openpyxl
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def close_popup():
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'takeover-close')))

        # Cerrar el cuadro de diálogo emergente
        close_button = driver.find_element(By.ID, 'takeover-close')
        close_button.click()
    except Exception as e:
        print(f"No hay pop-up para cerrar")


def write_movie_data(sheet, date, country, cinema_brand, cinema_location, movie_title, time, language, classification):
    next_row = sheet.max_row + 1
    sheet.cell(row=next_row, column=1).value = date
    sheet.cell(row=next_row, column=2).value = country
    sheet.cell(row=next_row, column=3).value = cinema_brand
    sheet.cell(row=next_row, column=4).value = cinema_location
    sheet.cell(row=next_row, column=5).value = movie_title
    sheet.cell(row=next_row, column=6).value = time
    sheet.cell(row=next_row, column=7).value = language
    sheet.cell(row=next_row, column=8).value = classification


def scrape_movie_details(movie_listing):
    # Extraer el título de la película
    try:
        movie_title_element = movie_listing.find_element(
            By.CSS_SELECTOR, ".informacion-general h3")
    except:
        movie_title_element = movie_listing.find_element(
            By.CSS_SELECTOR, "header h3 a")

    movie_title = movie_title_element.text.strip()

    # Extraer los formatos y sus horarios
    formats_with_times = {}
    try:
        format_elements = movie_listing.find_elements(
            By.CSS_SELECTOR, ".formatos .formato")

        if format_elements:

            for format_element in format_elements:
                # Verifica si hay una imagen que indique el formato "3D"
                formato_imagen_div = format_element.find_elements(
                    By.CSS_SELECTOR, ".formato-imagen")
                if formato_imagen_div:
                    formato_imagen = formato_imagen_div[0].find_element(
                        By.TAG_NAME, "img")
                    imagen_alt = formato_imagen.get_attribute("alt")
                    if '3D' in imagen_alt:
                        format_type = "3D"
                    elif 'junior' in imagen_alt:
                        format_type = "Junior"
                    else:
                        format_type = "2D"
                else:
                    format_type = "2D"

                # Obtén el nombre del formato (SUB o DOB) y combínalo con el tipo (2D o 3D)
                format_name = format_element.find_element(
                    By.CSS_SELECTOR, ".formato-nombre").text.strip()

                # Obtén los horarios

                times = [a.text.strip() for a in format_element.find_elements(
                    By.CSS_SELECTOR, ".horas a p")]

                if format_name in formats_with_times:
                    formats_with_times[format_name].append(
                        (times, format_type))
                else:
                    formats_with_times[format_name] = [(times, format_type)]
        else:
            raise NoSuchElementException

    except NoSuchElementException:
        format_elements = movie_listing.find_elements(
            By.CSS_SELECTOR, ".horarioExp")

        for format_element in format_elements:
            times = [a.text.strip() for a in format_element.find_elements(
                By.CSS_SELECTOR, "time a")]

            format_type = format_element.find_element(
                By.CSS_SELECTOR, "p span").text.strip().replace("\n", "").replace("\r", "")

            if format_type != "3D":
                format_type = "2D"

            format_name = format_element.get_attribute("class").split()[-1]

            if format_name in formats_with_times:
                formats_with_times[format_name].append((times, format_type))
            else:
                formats_with_times[format_name] = [(times, format_type)]

    return movie_title, formats_with_times

current_date_ = datetime.date.today().strftime('%d-%m-%Y')
cinepolis_urls = [
    "https://cinepolis.com.sv/",
    "https://cinepolis.com.gt",
    "https://cinepolis.co.cr/",
    "https://cinepolis.com.pa/"
]
# Crear libro de trabajo, hoja y fila de encabezados
workbook = openpyxl.Workbook()
sheet = workbook.active

next_row = 1

sheet.cell(row=next_row, column=1).value = "Fecha"
sheet.cell(row=next_row, column=2).value = "Pais"
sheet.cell(row=next_row, column=3).value = "Cine"
sheet.cell(row=next_row, column=4).value = "Nombre Cine"
sheet.cell(row=next_row, column=5).value = "Titulo"
sheet.cell(row=next_row, column=6).value = "Hora"
sheet.cell(row=next_row, column=7).value = "Idioma"
sheet.cell(row=next_row, column=8).value = "Formato"

# Crear una nueva instancia de Options
edge_options = Options()
edge_options.add_argument("--inprivate")
edge_options.add_argument("--start-maximized")

path = 'C:/Users/Wizar/Documents/Curso de Business Intelligence y Big Data Febrero 2024/Proyecto Final/msedgedriver.exe'

# Configurar el servicio Edge y crear el controlador
service = Service(executable_path=path)
driver = webdriver.Edge(service=service, options=edge_options)

for url in cinepolis_urls:
    # Navegar a la página web
    driver.get(url)
    driver.implicitly_wait(5)
    close_popup()

    # seleccionar ciudad
    try:
        select = Select(driver.find_element(By.ID, 'ciudad'))

    except NoSuchElementException:
        try:
            select = Select(driver.find_element(By.ID, 'cmbCiudades'))

        except NoSuchElementException:
            print("Ninguno de los IDs fue encontrado.")

    options = select.options

    driver.implicitly_wait(5)

    for i, option in enumerate(options):
        select.select_by_index(i)

        selected_option = select.first_selected_option
        location_text = selected_option.text
        country = location_text.split(', ')[-1]

        if country == 'Jutiapa' or country == 'Zacapa' or country == 'San Pedro Carchá':
            country = 'Guatemala'
        elif country == 'David Chiriquí':
            country = 'Panamá'

        try:
            button_element = driver.find_element(
                By.CSS_SELECTOR, "button[type='submit']")

        except:
            try:
                button_element = driver.find_element(
                    By.CSS_SELECTOR, ".btnEnviar[type='submit']")

            except:
                print(f"No se pudo encontrar el botón o el input: {e}")

        button_element.click()

        # Encuentra todos los elementos que contienen información de un cine
        try:
            cinemas = driver.find_elements(
                By.CSS_SELECTOR, "#listBillboards .ScheduleMovie__ScheduleMovieComponent-sc-7752wm-0")

            if not cinemas:
                raise NoSuchElementException
        except NoSuchElementException:
            try:
                wait = WebDriverWait(driver, 10)
                cinemas = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".divComplejo")))

            except:
                print("Ningun elemento fue encontrado.")

        # Itera a través de cada cine
        for movie in cinemas:
            try:
                cinema_element = movie.find_element(
                    By.CSS_SELECTOR, "header[id^='cinema-']")
                cinema_name = cinema_element.find_element(
                    By.TAG_NAME, "h2").text
                cinema_name_parts = cinema_name.split(" ")
                cinema_brand = cinema_name_parts[0].capitalize()
                cinema_location = " ".join(cinema_name_parts[1:]).title()

            except NoSuchElementException:
                try:
                    cinema_element = movie.find_element(
                        By.CSS_SELECTOR, ".divFecha")
                    cinema_name = cinema_element.find_element(
                        By.TAG_NAME, "h2").text
                    cinema_name_parts = cinema_name.split(" ")
                    cinema_brand = cinema_name_parts[0].capitalize()
                    cinema_location = " ".join(cinema_name_parts[1:]).title(
                    ).strip().replace("\n", "").replace("\r", "")
                    cinema_location = cinema_location[:-1].strip()

                except:
                    print('No se encontro ninguna lista de peliculas')

            try:
                list_movies = movie.find_element(By.CLASS_NAME, "movies")
                movie_elements = list_movies.find_elements(
                    By.CSS_SELECTOR, ".SingleScheduleMovie__SingleScheduleComponent-sc-1n3hti2-0")

                if not movie_elements:
                    raise NoSuchElementException
            except NoSuchElementException:
                movie_elements = movie.find_elements(
                    By.CSS_SELECTOR, "article.row.tituloPelicula")

            for movie_listing in movie_elements:
                # Extraer los detalles de la película
                movie_title, formats_with_times = scrape_movie_details(
                    movie_listing)

                # Escribir los datos de la película en la hoja de Excel para cada horario
                for format_name, times_with_type in formats_with_times.items():
                    for times, format_type in times_with_type:
                        for time in times:
                            # Escribir los datos en el Excel:
                            write_movie_data(sheet, datetime.date.today().strftime(
                                '%d-%m-%Y'), country, cinema_brand, cinema_location, movie_title, time, format_name, format_type)

        # Volver a la página principal para seleccionar la siguiente opción
        driver.get(url)

        # seleccionar ciudad
        try:
            select = Select(driver.find_element(By.ID, 'ciudad'))
        except NoSuchElementException:
            try:
                select = Select(driver.find_element(By.ID, 'cmbCiudades'))
            except NoSuchElementException:
                print("Ninguno de los IDs fue encontrado.")

        # Guardar el libro de trabajo de Excel
        current_hour = datetime.datetime.now().strftime('%H-%M-%S')
        distin_name = "results/cinepolis-"+str(current_date_) + \
            " "+str(current_hour)+".xlsx"
        workbook.save(filename=distin_name)
        print("Información de los cines guardada en el archivo Excel.")

# Salir del controlador
driver.quit()
