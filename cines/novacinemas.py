from config_selenium import *

driver.get('https://www.novacinemas.cr/')

driver.maximize_window()

time.sleep(2)
cines = 3
country = "Costa Rica"
cinema_brand = "Nova Cinemas"
cine_name = ""
current_date_ = datetime.date.today().strftime('%d-%m-%Y')

#moverse a cartelera
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
        current_date_dropdown = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[2]/nav')
        current_date_dropdown.click()

        curren_day = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div[2]/nav/ul/li[2]')
        curren_day.click()
    except Exception as e:
        print(f"No se pudo seleccionar la fecha actual")

def select_all_movies_by_class(): 
    try:
        all_movies = driver.find_elements(By.XPATH, '//div[contains(@class, "schedules-accordion") and contains(@class, "ui-accordion") and contains(@class, "ui-widget") and contains(@class, "ui-helper-reset")]')
        print(len(all_movies))
        # !!!!!!!  NO FUNCIONA !!!!!!!
        
    except Exception as e:
        print(f"No se pudieron seleccionar todas las peliculas")

for i in range(cines):
    display_all_cines()
    select_cine(i)
    select_current_date()
    select_all_movies_by_class()




    #limpiar nombre del cine
    cine_name = ""

