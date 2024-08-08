import os
from config_selenium import *

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
sheet.cell(row=next_row, column=7).value = "Formato"
sheet.cell(row=next_row, column=8).value = "Idioma"


driver.get('https://www.novacinemas.cr/')
driver.maximize_window()

time.sleep(1)
country = "Costa Rica"
cinema_brand = "Nova Cinemas"
current_date_ = datetime.date.today().strftime('%d-%m-%Y')
movies_info = []

def init_process():
    #choose cinema
    cinemas_dropdown = driver.find_element(By.XPATH, '/html/body/header/section[1]/div/div[2]/nav/a')
    cinemas_dropdown.click()
    time.sleep(1)
    # Encuentra el elemento <ul> por su ID
    ul_element = driver.find_element(By.ID, "menu-cines")
    return ul_element

parent_ul = init_process()
# Encuentra todos los elementos <a> dentro del <ul>
links = parent_ul.find_elements(By.TAG_NAME, "a")

# Itera sobre cada enlace y visita la URL
for link in range(len(links)):
    try:
        if link != 0:
            parent_ul = init_process()
            # Encuentra todos los elementos <a> dentro del <ul>
            links = parent_ul.find_elements(By.TAG_NAME, "a")
        
        cine_name = "Nova Cinemas "+links[link].text
        
        url = links[link].get_attribute("href")
        #print(f"Visitando: {url}")
        driver.get(url)
        time.sleep(2)
    except Exception as e:
        print(f"Error: {e}")

    try:
        cartelera = driver.find_element(By.CSS_SELECTOR, ".row.cinema.view.movie.cinemaBlock")
        # Encuentra todos los h2 con la clase "title" dentro del div "cartelera"
        titulos_coleccion = cartelera.find_elements(By.CSS_SELECTOR,"h2.title")
        
        # Imprime los nombres de las películas
        for index in range(len(titulos_coleccion)):

            titulo = titulos_coleccion[index].text
            #print(f"Película: {titulo}")
            
            items_list = cartelera.find_elements(By.CSS_SELECTOR, '.rowTimes.ui-accordion-content.ui-corner-bottom.ui-helper-reset.ui-widget-content.ui-accordion-content-active')
            
            format_elements = items_list[index].find_elements(By.CSS_SELECTOR, 'span')
            hour_elements = items_list[index].find_elements(By.CSS_SELECTOR, 'a.btn-hourId')
            
            # Separar formato y lenguaje
            for format_element in format_elements:
                format_text = format_element.text.split()
                if len(format_text) == 2:
                    movie_format = format_text[0]
                    language = format_text[1]
                else:
                    movie_format = format_text[0]
                    language = "DOB"  # Valor por defecto si solo hay un formato
                    
            times = [hour_element.text for hour_element in hour_elements]

            # Agregar la información a la lista
            for time_loop in times:
                movies_info.append([current_date_, country, cinema_brand, cine_name, titulo, time_loop, movie_format, language])
             # Insertar la información en la hoja de cálculo
            for movie in movies_info:
                next_row += 1
                sheet.cell(row=next_row, column=1).value = movie[0]
                sheet.cell(row=next_row, column=2).value = movie[1]
                sheet.cell(row=next_row, column=3).value = movie[2]
                sheet.cell(row=next_row, column=4).value = movie[3]
                sheet.cell(row=next_row, column=5).value = movie[4]
                sheet.cell(row=next_row, column=6).value = movie[5]
                sheet.cell(row=next_row, column=7).value = movie[6]
                sheet.cell(row=next_row, column=8).value = movie[7]
            movies_info.clear()
            
    except Exception as e:
        print(f"Error: {e}")
        continue

    driver.back()
    time.sleep(1)


if not os.path.exists('results'):
    os.makedirs('results')

# Guardar el archivo
current_hour = datetime.datetime.now().strftime('%H-%M-%S')
distin_name = "results/novacinemas_"+str(current_date_) + \
            "_"+str(current_hour)+".xlsx"
workbook.save(filename=distin_name)
