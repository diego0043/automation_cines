from config_selenium import *

driver.get('https://www.novacinemas.cr/')

driver.maximize_window()

time.sleep(2)
cines = 3
country = "Costa Rica"
cinema_brand = "Nova Cinemas"
cine_name = ""
current_date_ = datetime.date.today().strftime('%d-%m-%Y')

# moverse a cartelera
cartelera = driver.find_element(By.XPATH, '//*[@id="menu-item-103"]/a')
cartelera.click()


def write_movie_data(sheet, date, country, cinema_brand, cinema_location, movie_title, time, classification, language):
    next_row = sheet.max_row + 1
    sheet.cell(row=next_row, column=1).value = date
    sheet.cell(row=next_row, column=2).value = country
    sheet.cell(row=next_row, column=3).value = cinema_brand
    sheet.cell(row=next_row, column=4).value = cinema_location
    sheet.cell(row=next_row, column=5).value = movie_title
    sheet.cell(row=next_row, column=6).value = time
    sheet.cell(row=next_row, column=7).value = classification
    sheet.cell(row=next_row, column=8).value = language


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


def waitingPage():
    # Esperar a que la página se cargue completamente (ajustar según necesidad)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body')))


def select_cine(position):
    try:
        id_cine = 'ui-id-' + str(position+1)
        cine = driver.find_elements(By.ID, id_cine)
        cine_name = cine[0].text
        cine[0].click()
    except Exception as e:
        print(f"No se pudo seleccionar el cine {position}")


def display_all_cines():
    try:
        cines_option = driver.find_element(By.ID, 'select')
        cines_option.click()
    except Exception as e:
        print(f"No se pudieron desplegar todos los cines")


def select_current_date():
    try:
        current_date_dropdown = driver.find_element(
            By.XPATH, '/html/body/main/div/div[1]/div[2]/nav')
        current_date_dropdown.click()

        curren_day = driver.find_element(
            By.XPATH, '/html/body/main/div/div[1]/div[2]/nav/ul/li[2]')
        curren_day.click()
    except Exception as e:
        print(f"No se pudo seleccionar la fecha actual")


def select_all_movies_by_class(position_cine):
    try:
        init_div = 2 # rango: 0 - n
        init_div_tanda = 1 # rango: 0 - n
        init_div_tanda_col = 1 # rango: 0 - 2

        if position_cine == 0:

            # iteramos sobre todos los componentes padres de las peliculas
            xpath_movie = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[5]/ul/div[2]/li/div['+str(
                init_div)+']/div[2]/div/h3')
            

        elif position_cine == 1:

            # iteramos sobre todos los componentes padres de las peliculas
            xpath_movie = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[7]/ul/div[1]/li/div['+str(
                init_div)+']/div[2]/div/h3')

            # iteramos sobre todos los componentes padres de las tandas dentro de las peliculas
            xpath_tanda = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[7]/ul/div[1]/li/div['+str(init_div)+']/div[2]/div/div/div/div['+str(
                init_div_tanda)+']/div['+str(init_div_tanda_col)+']')

        elif position_cine == 2:
            xpath_movie = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[9]/ul/div[1]/li/div['+str(
                init_div)+']/div[2]/div/h3')

            # iteramos sobre todos los componentes padres de las tandas dentro de las peliculas
            xpath_tanda = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[9]/ul/div[2]/li/div[2]/div[2]/div/div/div/div/div['+str(init_div_tanda_col)+']')


        # bandera para saber si existen peliculas y poder salir del ciclo
        exist_movies = True

        # bandera para saber si existen funciones y poder salir del ciclo 2
        exist_functions = True

        # bandera para saber si existen funciones y poder salir del ciclo 3
        exist_functions_tanda = True  

        while exist_movies:

            # limpiar nombre de la pelicula y eliminar la calificacion
            title_split = xpath_movie.text.rfind(" ")
            title = xpath_movie.text[:title_split]
            print( "Movie actual: " + title)

            init_div += 1
            try:
                if position_cine == 0:

                    # buscar la pelicula para el cine 1
                    xpath_movie = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[5]/ul/div[2]/li/div['+str(
                        init_div)+']/div[2]/div/h3')
                    
                    if xpath_movie:
                        while exist_functions:

                            while exist_functions_tanda: 
                                try: 
                                    # buscar la tanda para la sala 1
                                    path_ = '/html/body/main/div/div[1]/div[5]/ul/div[2]/li/div['+str(init_div - 1)+']/div[2]/div/div/div/div['+str(init_div_tanda)+']/div['+str(init_div_tanda_col)+']'
                                    xpath_tanda = driver.find_element(By.XPATH, path_)
                                    init_div_tanda_col += 1
                                    print(xpath_tanda.text)
                                except Exception as e:
                                    print("No hay mas tandas para esta funcion")
                                    exist_functions_tanda = False

                            try:
                                init_div_tanda_col = 1
                                init_div_tanda += 1
                                path_ = '/html/body/main/div/div[1]/div[5]/ul/div[2]/li/div['+str(init_div - 1)+']/div[2]/div/div/div/div['+str(init_div_tanda)+']/div['+str(init_div_tanda_col)+']'
                                # buscar la tanda para la sala 1
                                print(path_)
                                xpath_tanda = driver.find_element(By.XPATH, path_)
                                print(xpath_tanda.text)
                                init_div_tanda_col += 1
                                exist_functions_tanda = True
                            except Exception as e:

                                print("No hay mas tandas 2")
                                exist_functions = False
                                init_div_tanda_col = 1
                                init_div_tanda = 1
                        
                        exist_functions = True

                elif position_cine == 1:

                    # buscar la pelicula para el cine 2
                    xpath_movie = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[7]/ul/div[1]/li/div['+str(
                        init_div)+']/div[2]/div/h3')

                elif position_cine == 2:

                    # buscar la pelicula para el cine 3
                    xpath_movie = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[9]/ul/div[1]/li/div['+str(
                        init_div)+']/div[2]/div/h3'
                    )

            except Exception as e:
                exist_movies = False

    except Exception as e:
        print(f"No se pudieron seleccionar todas las peliculas")


for i in range(cines):
    display_all_cines()
    select_cine(i)
    select_current_date()
    select_all_movies_by_class(i)
    print(i)

    # limpiar nombre del cine
    cine_name = ""
