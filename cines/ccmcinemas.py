from config_selenium import *

# Abrir la página web
driver.get('https://ccmcinemas.com/')

# Maximizar la ventana del navegador (opcional)
driver.maximize_window()

# Esperar unos segundos para asegurarse de que la página se cargue completamente (opcional)
time.sleep(2)

# Encontrar todos los elementos <a> que contienen enlaces a diferentes cines
links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/cines/"]')
cartelera = ""
country = "Costa Rica"
cinema_brand = "CCM Cinemas"


def write_movie_data(sheet, date, country, cinema_brand, cinema_location, movie_title, language):
    next_row = sheet.max_row + 1
    sheet.cell(row=next_row, column=1).value = date
    sheet.cell(row=next_row, column=2).value = country
    sheet.cell(row=next_row, column=3).value = cinema_brand
    sheet.cell(row=next_row, column=4).value = cinema_location
    sheet.cell(row=next_row, column=5).value = movie_title
    sheet.cell(row=next_row, column=7).value = language

# Crear libro de trabajo, hoja y fila de encabezados
workbook = openpyxl.Workbook()
sheet = workbook.active

next_row = 1

sheet.cell(row=next_row, column=1).value = "Fecha"
sheet.cell(row=next_row, column=2).value = "Pais"
sheet.cell(row=next_row, column=3).value = "Cine"
sheet.cell(row=next_row, column=4).value = "Nombre Cine"
sheet.cell(row=next_row, column=5).value = "Titulo"
sheet.cell(row=next_row, column=7).value = "Idioma"

def close_popup():
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.spu-close')))
        # Cerrar el cuadro de diálogo emergente
        close_button = driver.find_element(By.CSS_SELECTOR, '.spu-close')
        close_button.click()
    except Exception as e:
        print(f"No hay pop-up para cerrar")


def return_home():
    driver.get('https://ccmcinemas.com/')


def waitingPage():
    # Esperar a que la página se cargue completamente (ajustar según necesidad)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body')))


def moveIframe():
    # Espera hasta que el iframe esté presente y cambia al contexto del iframe
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, 'CCMTANDAS'))
    )


def moveCartelera():
    cartelera = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "CARTELERA")]')))
    cartelera.click()


# Iterar sobre los elementos encontrados
for i in range(len(links)):
    # Volver a encontrar los elementos <a> después de cada iteración para evitar StaleElementReferenceException
    links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/cines/"]')

    # Obtener el URL del cine
    cine_url = links[i].get_attribute('href')

    # Navegar a la URL del cine
    driver.get(cine_url)

    waitingPage()

    try:
        close_popup()

        # Moverse a la sección de la cartelera
        moveCartelera()

        waitingPage()

        # Encontrar todos los botones con la clase especificada
        botones = driver.find_elements(
            By.CSS_SELECTOR, 'a._self.pt-cv-readmore.btn.btn-success')

        # Hacer clic en cada botón utilizando índices
        for j in range(len(botones)):
            try:
                waitingPage()
                # Asegurarse de volver al contexto principal después de cada iteración
                driver.switch_to.default_content()

                # Volver a encontrar los botones después de cada interacción
                botones = driver.find_elements(
                    By.CSS_SELECTOR, 'a._self.pt-cv-readmore.btn.btn-success')
                boton = botones[j]

                boton.click()
                waitingPage()

                try:
                    moveIframe()

                    lista_tandas_elements = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.CLASS_NAME, 'TandasHoraCalendario'))
                    )

                    for m in range(len(lista_tandas_elements)):
                        try:
                            # Volver a encontrar los botones después de cada interacción
                            lista_btn_hora = WebDriverWait(driver, 10).until(
                                EC.presence_of_all_elements_located(
                                    (By.CLASS_NAME, 'TandasHoraCalendario'))
                            )
                            btn_hora = lista_btn_hora[m]
                            btn_hora.click()

                            # Extraer la información de la tanda
                            nameMovie = driver.find_element(
                                By.ID, 'ContentPlaceHolder1_lblPelicula').text
                            nameCine = driver.find_element(
                                By.ID, 'ContentPlaceHolder1_lblCine').text
                            typeCensura = driver.find_element(
                                By.ID, 'ContentPlaceHolder1_lblCensura').text
                            tanda = driver.find_element(
                                By.ID, 'ContentPlaceHolder1_lblHorario').text
                            moveDay = driver.find_element(By.ID, 'ContentPlaceHolder1_lblFecha').text
                            write_movie_data(sheet, country, country, cinema_brand, nameCine, nameMovie, tanda)

                            # Volver a la página de la cartelera
                            return_tandas = driver.find_element(By.ID, 'A1')
                            return_tandas.click()
                        except Exception as e:
                            print(
                                f"Error al extraer la información de la tanda: {e}")

                except Exception as e:
                    print(f"Error al extraer la información: {e}")

                # Asegurarse de volver al contexto principal después de cada iteración
                driver.switch_to.default_content()

                # Volver a la página de la cartelera
                moveCartelera()
                waitingPage()
            except Exception as e:
                print(f"Error al hacer clic en el botón: {e}")

        # Volver a la página inicial
        return_home()
        waitingPage()
    except Exception as e:
        print(f"Error en la página del cine: {e}")

# Guardar el libro de trabajo de Excel
workbook.save(filename="ccmcinemas.xlsx")
print("Información de los cines guardada en el archivo Excel.")
