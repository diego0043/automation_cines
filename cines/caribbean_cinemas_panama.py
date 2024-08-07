from config_selenium import *

driver.get('https://caribbeancinemas.com/location/panama/')

driver.maximize_window()

time.sleep(2)
cines = 2
country = "Panamá"
cinema_brand = "Caribbean Cinemas"
cine_name = ""
current_date_ = datetime.date.today().strftime('%d-%m-%Y')
list_all = []


def select_cine(position):
    try:
        # moverse a cartelera
        cartelera = driver.find_element(
            By.XPATH, '/html/body/div[1]/header/div/div/nav/ul/li[5]')

        # Crear una instancia de ActionChains
        actions = ActionChains(driver)

        # Realizar la acción de hover
        actions.move_to_element(cartelera).perform()

        # Esperar a que aparezca el menú desplegable
        waitingPage()

        cine = driver.find_element(
            By.XPATH, f'/html/body/div[1]/header/div/div/nav/ul/li[5]/ul/li[{position+1}]/a')

        cine_name = cine.text
        cine.click()
        time.sleep(2)
        return cine_name

    except Exception as e:
        print(f"No se pudo seleccionar el cine {position}")


def get_movies(position, cine_name_):
    movies = driver.find_elements(By.CLASS_NAME, 'three-fourth')

    for i in range(len(movies)):
        try:
            if position == 0:
                movie_title = driver.find_element(
                    By.XPATH, f'/html/body/div[1]/div[2]/div/main/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[{i+1}]/div/div/div[2]/h1')
                name_movie = movie_title.text
                try:

                    format_movie = ""
                    format_plus = driver.find_element(
                        By.XPATH, f'/html/body/div[1]/div[2]/div/main/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[{i+1}]/div/div/div[2]/h1/b/img')
                    image_src = format_plus.get_attribute("src")

                    pattern = re.compile(r"(CXC|premium)")
                    match = pattern.search(image_src)

                    if match:
                        if match.group(1) == "CXC":
                            format_movie = "2D CXC"
                        else:
                            format_movie = "2D Premium"
                    else:
                        format_movie = "2D"

                except Exception as e:
                    format_movie = "2D"

                lenguage = "Dob"
                exist_tanda = True
                bandera = 1
                while exist_tanda:
                    try:
                        tanda = driver.find_element(
                            By.XPATH, f'/html/body/div[1]/div[2]/div/main/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[{i+1}]/div/div/div[2]/div[2]/a[{bandera}]')
                        list_all.append(
                            [current_date_, country, cinema_brand, cine_name_, name_movie, tanda.text, format_movie, lenguage])
                        bandera += 1
                    except Exception as e:
                        print(
                            f"No hay más tandas para la película {movie_title.text}")
                        exist_tanda = False

            else:

                movie_title = driver.find_element(
                    By.XPATH, f'/html/body/div[1]/div[2]/div/main/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[{i+1}]/div/div/div[2]/h1')
                name_movie = movie_title.text
                format_movie = "2D"
                lenguage = "Dob"
                exist_tanda = True
                bandera = 1

                while exist_tanda:
                    try:
                        tanda = driver.find_element(
                            By.XPATH, f'/html/body/div[1]/div[2]/div/main/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[{i+1}]/div/div/div[2]/div[2]/a[{bandera}]')
                        list_all.append(
                            [current_date_, country, cinema_brand, cine_name_, name_movie, tanda.text, format_movie, lenguage])
                        bandera += 1
                    except Exception as e:
                        print(
                            f"No hay más tandas para la película {movie_title.text}")
                        exist_tanda = False
        except Exception as e:
            print(f"No se pudo obtener la información de la película {i}")


def waitingPage():
    # Esperar a que la página se cargue completamente (ajustar según necesidad)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body')))


def add_data_to_excel(list):
    for i in range(len(list)):
        write_movie_data(sheet, list[i][0], list[i][1], list[i][2],
                         list[i][3], list[i][4], list[i][5], list[i][6], list[i][7])


for i in range(cines):
    cine_name = select_cine(i)
    cine_name = cinema_brand + " | " + cine_name
    get_movies(i, cine_name)
    driver.back()

add_data_to_excel(list_all)

current_hour = datetime.datetime.now().strftime('%H-%M-%S')
distin_name = "results/caribbean_cinemas_panama-"+str(current_date_) + \
    " "+str(current_hour)+".xlsx"
workbook.save(filename=distin_name)
print("Informacion de los cines guardada en el archivo Excel.")
