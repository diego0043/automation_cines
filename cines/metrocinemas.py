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

#Start the browser
driver.maximize_window()
driver.get('https://www.metrocinemas.hn/main.aspx#')
time.sleep(2)

# Variables
country = "Honduras"
cinema_brand = "Metrocinemas"

def get_cinema():
    try:
        # Localiza el elemento padre inicial
        a_menu_lateral = driver.find_element(By.XPATH, '//*[@id="cd-menu-trigger"]')
        a_menu_lateral.click()
        time.sleep(2)
        # Obtener los elementos <a> dentro del ul de la cartelera
        get_cartelera = driver.find_element(By.XPATH, '//*[@id="cd-lateral-nav"]/ul[1]/li/a')
        get_cartelera.click()
    except Exception as e:
        print(f"Error al interactuar con los elementos del menú: {e}")

li_cine = driver.find_elements(By.XPATH, '//*[@id="cd-lateral-nav"]/ul[1]/li/ul/li')

# Lista para almacenar la información de las películas
movies_info = []

for index in range(len(li_cine)):
    try:
        get_cinema()  #abrir el menú lateral
        time.sleep(2)
        # Re-localizar todos los elementos <li> cada vez
        li_cine = driver.find_elements(By.XPATH, '//*[@id="cd-lateral-nav"]/ul[1]/li/ul/li')
        # Encuentra la etiqueta <a> dentro del <li> actual
        a_tag = li_cine[index].find_element(By.TAG_NAME, 'a')

        cine_name =  "Metrocinemas " + a_tag.text
        date = datetime.date.today().strftime('%d-%m-%Y')

        # Hacer clic en la etiqueta <a>
        a_tag.click()
        time.sleep(2)  # Espera un segundo entre clics para evitar sobrecargar el navegador

        # Aquí puedes añadir lógica para obtener información de la película 
        divs_info = driver.find_elements(By.CSS_SELECTOR, '.col-md-4.col-sm-6.col-xs-12.combopelicartelera')

        for div in divs_info:
            # Obtén el título
            title_element = div.find_element(By.CSS_SELECTOR, '.combopelititulo h2')
            title = title_element.text.strip()

            # Obtén el idioma
            language_element = div.find_element(By.CSS_SELECTOR, '.icosdetalle img[src*="icos-38.jpg"] + p')
            language = language_element.text.strip()

            # Obtén el formato
            format_element = div.find_element(By.CSS_SELECTOR, '.icosdetalle img[src*="icos-42.png"] + p')
            format_movie = format_element.text.strip()

            # Obtén las horas de la película
            time_elements = div.find_elements(By.CSS_SELECTOR, '.horarioscartelera li.func-horario a')
            for time_element in time_elements:
                time_text = time_element.text.strip()
                # Agrega la información a la lista
                movies_info.append({
                    'date': date,
                    'country': country,
                    'cinema_brand': cinema_brand,
                    'cine_name': cine_name,
                    'title': title,
                    'language': language,
                    'time': time_text,
                    'format': format_movie
                })
        
        for movie in movies_info:
            print(movie)

        movies_info.clear()
        '''
        print("Lista de películas:", movies_info)

        '''
        # y agregarla a movies_info si es necesario
        driver.get('https://www.metrocinemas.hn/main.aspx#')
        time.sleep(2)  # Espera un segundo para asegurarse de que la página se haya cargado correctamente
        
    except:
        print("Error al interactuar con los elementos de la cartelera")



