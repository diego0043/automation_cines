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


driver.get('https://cinestar.com.gt/')

driver.maximize_window()

time.sleep(2)
country = "Guatemala"
cinema_brand = "cinestar"
current_date_ = datetime.date.today().strftime('%d-%m-%Y')


# Localiza el elemento padre inicial
parent_li_xpath = '//*[@id="menu-main-menu"]/li[5]'

# Simula el movimiento del mouse sobre el elemento padre para hacer visible el ul
def hover_over_menu():
    parent_li = driver.find_element(By.XPATH, parent_li_xpath)
    actions = ActionChains(driver)
    actions.move_to_element(parent_li).perform()
    return parent_li

parent_li = hover_over_menu()

# Obtener los elementos <a> dentro del ul
a_elements = parent_li.find_elements(By.XPATH, './/ul/li/a')

# Lista para almacenar la información de las películas
movies_info = []

# Iterar sobre cada elemento <a>, hacer clic en ellos, volver atrás y continuar con el siguiente enlace
for i in range(len(a_elements)):
    parent_li = hover_over_menu()
    a_elements = parent_li.find_elements(By.XPATH, './/ul/li/a')

    # Obtener el href del enlace
    href = a_elements[i].get_attribute('href')
    #print(f"Visiting: {href}")

    # Hacer clic en el enlace
    a_elements[i].click()

    # Esperar a que la nueva página cargue
    time.sleep(2)

     # Extraer información de la página de la película
    try:
        rows = driver.find_elements(By.CLASS_NAME, 'row.formats')
        
        for row in rows:
            cine_name = "Cine Star "+row.find_element(By.XPATH, '//*[@id="cineinfo"]/div/h2/b').text
            date = datetime.date.today().strftime('%d-%m-%Y')
            title = row.find_element(By.CSS_SELECTOR, 'div.column.three-fourth h1').text
            language = row.find_element(By.CSS_SELECTOR, 'div.column.three-fourth h5 i').text
            time_elements = row.find_elements(By.CSS_SELECTOR, 'div.column.three-fourth div a.myButton21')
            times = [time_element.text for time_element in time_elements]
            
            
            # El formato no se encuentra en la estructura HTML proporcionada, así que lo dejamos como "Empty"
            format_ = "2D"

            # Agregar la información a la lista
            for time_loop in times:
                movies_info.append([date, country, cinema_brand, cine_name, title, time_loop, format_, language])
            #print(movies_info)

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
        print(f"Error extracting data: {e}")

    # Volver atrás
    driver.back()

    # Esperar a que la página original vuelva a cargar
    time.sleep(2)

# Guardar el archivo
current_hour = datetime.datetime.now().strftime('%H-%M-%S')
distin_name = "results/cine_star-"+str(current_date_) + \
            " "+str(current_hour)+".xlsx"
workbook.save(filename=distin_name)
