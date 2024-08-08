from config_selenium import *

driver.get('https://www.novacinemas.cr/')

driver.maximize_window()

time.sleep(2)
cines = 3
country = "Costa Rica"
cinema_brand = "Nova Cinemas"
cine_name = ""
current_date_ = datetime.date.today().strftime('%d-%m-%Y')
list_all = []

# moverse a cartelera
cartelera = driver.find_element(By.XPATH, '//*[@id="menu-item-103"]/a')
cartelera.click()


def waitingPage():
    # Esperar a que la página se cargue completamente (ajustar según necesidad)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body')))


def select_cine(position):
    try:
        id_cine = 'ui-id-' + str(position+1)
        cine = driver.find_elements(By.ID, id_cine)
        for i in cine:
            cine_name = i.text
        cine[0].click()
        return cine_name
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


def separar_datos(texto):
    # Expresión regular para encontrar la hora (HH:MM AM/PM)
    patron_hora = re.compile(r'\b\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?\b')
    hora = patron_hora.search(texto).group(
    ) if patron_hora.search(texto) else "00:00"

    # Quitar la hora del texto para separar el formato y el doblaje
    resto = texto.replace(hora, '').strip() if hora else texto

    # Asumimos que el formato y doblaje están separados por un espacio
    partes = resto.split()
    formato = partes[0] if len(partes) > 0 else "2D"
    doblaje = ' '.join(partes[1:]) if len(partes) > 1 else "Dob"

    return hora, formato, doblaje


def select_all_movies_by_method(position_cine, cine_name):
    try:
        init_div = 2  # rango: 0 - n
        init_div_tanda = 1  # rango: 0 - n
        init_div_tanda_col = 1  # rango: 0 - n

        # bandera para saber si existen peliculas y poder salir del ciclo
        exist_movies = True

        # bandera para saber si existen funciones y poder salir del ciclo 2
        exist_functions = True

        # bandera para saber si existen funciones y poder salir del ciclo 3
        exist_functions_tanda = True

        while exist_movies:

            init_div += 1

            try:
                cine_number = ''
                ul_start_xpath = ''
                cine_number = '5' if position_cine == 0 else '7' if position_cine == 1 else '9' if position_cine == 2 else 'Invalid'
                ul_start_xpath = '9' if position_cine == 0 else '8' if position_cine == 1 else '1' if position_cine == 2 else 'Invalid'

                # /html/body/main/div/div[1]/div[5]/ul/div[8]/li/div[2]/div[2]/div/div/div/div/div
                # buscar la pelicula para el cine 1
                xpath_movie__ = '/html/body/main/div/div[1]/div['+str(cine_number)+']/ul/div['+str(ul_start_xpath)+']/li/div['+str(
                    init_div-1)+']/div[2]/div/h3'
                
                xpath_movie = driver.find_element(By.XPATH, xpath_movie__)

                if xpath_movie:

                    i = 0
                    # limpiar nombre de la pelicula y eliminar la calificacion
                    title_split = xpath_movie.text.rfind(" ")
                    name_movie = xpath_movie.text[:title_split]

                    while exist_functions:

                        while exist_functions_tanda:
                            try:
                                if i == 0:
                                    init_div_tanda = 1
                                    init_div_tanda_col = 1
                                    i += 1

                                # buscar la tanda para la sala 1
                                path_ = '/html/body/main/div/div[1]/div['+str(cine_number)+']/ul/div['+str(ul_start_xpath)+']/li/div['+str(
                                    init_div - 1)+']/div[2]/div/div/div/div['+str(init_div_tanda)+']/div['+str(init_div_tanda_col)+']'
                                xpath_tanda = driver.find_element(
                                    By.XPATH, path_)

                                hora, formato, doblaje = separar_datos(
                                    xpath_tanda.text)

                                list_all.append(
                                    [current_date_, country, cinema_brand, cine_name, name_movie, hora, formato, doblaje])
                                init_div_tanda_col += 1

                            except Exception as e:
                                exist_functions_tanda = False

                        try:
                            init_div_tanda_col = 1
                            init_div_tanda += 1
                            path_ = '/html/body/main/div/div[1]/div['+str(cine_number)+']/ul/div['+str(ul_start_xpath)+']/li/div['+str(
                                init_div - 1)+']/div[2]/div/div/div/div['+str(init_div_tanda)+']/div['+str(init_div_tanda_col)+']'
                            # buscar la tanda para la sala 1
                            xpath_tanda = driver.find_element(
                                By.XPATH, path_)
                            exist_functions_tanda = True
                        except Exception as e:
                            exist_functions = False
                            init_div_tanda_col = 1
                            init_div_tanda = 1

                    exist_functions = True
                    exist_functions_tanda = True

            except Exception as e:
                exist_movies = False

    except Exception as e:
        print(f"No se pudieron seleccionar todas las peliculas")


def add_data_to_excel(list):
    for i in range(len(list)):
        write_movie_data(sheet, list[i][0], list[i][1], list[i][2],
                         list[i][3], list[i][4], list[i][5], list[i][6], list[i][7])

    list_all.clear()


for i in range(3):
    display_all_cines()
    cine_name = select_cine(i)
    select_current_date()
    select_all_movies_by_method(i, cine_name)

add_data_to_excel(list_all)


current_hour = datetime.datetime.now().strftime('%H-%M-%S')
distin_name = "results/novacinemas-"+str(current_date_) + \
    " "+str(current_hour)+".xlsx"
workbook.save(filename=distin_name)
print("Informacion de los cines guardada en el archivo Excel.")
