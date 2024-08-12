import os
from config_selenium import *
from selenium.common.exceptions import NoSuchElementException


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
driver.get('https://psiglonuevo.com/')
time.sleep(2)

# Variables
country = "Nicaragua"
cinema_brand = "Siglo Nuevo"
current_date_ = datetime.date.today().strftime('%d-%m-%Y')
movies_info = []


def get_movies():
    try:
        # Get movies by class
        movies_list = driver.find_elements(By.CSS_SELECTOR, '.fusion-no-lightbox')
        return movies_list

    except Exception as e:
        print(f"Error al interactuar con las peliculas: {e}")
    
movies = get_movies()

for movie in range(len(movies)):
    try:
        
        get_movie = get_movies()
        get_movie[movie].click()
        time.sleep(1)

        titulo = driver.find_element(By.CSS_SELECTOR, 'h2.title-heading-center.fusion-responsive-typography-calculated').text
        
        # Encontrar todos los elementos <a> dentro de la lista <ul> con la clase "nav-tabs" usando XPath
        enlaces = driver.find_elements(By.CSS_SELECTOR, '.tab-link')
        
        
        # Iterar sobre cada enlace y hacer clic en él
        for enlace in enlaces:


            if enlaces.index(enlace) == 2:
                break
            else:
                enlace.click();
                time.sleep(1)
                
                
                try:
                    tab_panes = driver.find_elements(By.CSS_SELECTOR, '.tab-pane')
                    #print(len(tab_panes))
                    for tab_pane in tab_panes:
                        
                        
                        if enlaces.index(enlace) == 0:
                            cine_name = "Siglo Nuevo León"
                            functions_today = tab_pane.find_element(By.XPATH, './/div[@align="center"][1]')
                            tanda_items = functions_today.find_elements(By.CLASS_NAME, 'tanda-item')
                        else:
                            cine_name = "Siglo Nuevo Chinandega"
                            functions_today = tab_pane.find_element(By.XPATH, './/div[@align="center"][1]')
                            tanda_items = functions_today.find_elements(By.CSS_SELECTOR, '.tandach-item')

                        for tanda in tanda_items:
                            texto = tanda.text
                            if "NO DISPONIBLE" in texto:
                                hora = "NO DISPONIBLE"
                                lenguaje = "NO DISPONIBLE"
                            else:
                                if "SUBT" in texto:
                                    hora, lenguaje = texto.rsplit(" ", 1)
                                elif "DOB" in texto:
                                    hora, lenguaje = texto.rsplit(" ", 1)
                                else:
                                    hora = texto
                                    lenguaje = "DOB"

                            #print(f"Hora: {hora}, Lenguaje: {lenguaje}")

                            movies_info.append([current_date_, country, cinema_brand, cine_name, titulo, hora, '2D', lenguaje])

                except NoSuchElementException:
                    # Manejar el caso en que el XPath no exista
                    fecha = "NO DISPONIBLE"
                    hora = "NO DISPONIBLE"
                    lenguaje = "NO DISPONIBLE"
                    movies_info.append([current_date_, country, cinema_brand, cine_name, titulo, hora, '2D', lenguaje])
                
        for movie in movies_info:
            next_row += 1
            try:
                sheet.cell(row=next_row, column=1).value = movie[0]
                sheet.cell(row=next_row, column=2).value = movie[1]
                sheet.cell(row=next_row, column=3).value = movie[2]
                sheet.cell(row=next_row, column=4).value = movie[3]
                sheet.cell(row=next_row, column=5).value = movie[4]
                sheet.cell(row=next_row, column=6).value = movie[5]
                sheet.cell(row=next_row, column=7).value = movie[6]
                sheet.cell(row=next_row, column=8).value = movie[7]
            except Exception as e:
                print(f"Error al insertar la información en la hoja de cálculo: {e}")

        #print(movies_info)
        movies_info.clear()
        
        time.sleep(2)
        driver.back()
        time.sleep(1)

    except Exception as e:
        print(f"Error al interactuar con las peliculas: {e}")


# Guardar el archivo
current_hour = datetime.datetime.now().strftime('%H-%M-%S')
distin_name = "results/siglo_nuevo-"+str(current_date_) + \
            " "+str(current_hour)+".xlsx"
workbook.save(filename=distin_name)


