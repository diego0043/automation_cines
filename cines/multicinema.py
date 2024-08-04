from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
import locale
import pandas as pd
from datetime import datetime

#funcion que servira para convertir la fecha al formato de mes-dia-año.
def date_conversion(date_movies):
    locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
    date_text=date_movies.text[22:]
    date_text=date_text.split()
    if(date_text[0]=="Miercoles"):
        date_text[0]="Miércoles"
    elif date_text[0]=="Sabado":
        date_text[0]="Sábado"
    date_text=" ".join(date_text)
    fecha_datetime=datetime.strptime(date_text, "%A %d %B %Y")
    fecha_formato=fecha_datetime.strftime("%m-%d-%Y")
    return fecha_formato

#función que estructura los datos
def cinema_data_analyzer(data, date, country):
    # Inicializa variables para almacenar la información temporalmente
    complejo = ""
    titulo = ""
    clasificacion = ""
    promocion = ""
    duracion = ""
    idioma = ""
    formato = ""
    horarios = []

    # Lista para almacenar filas de datos
    data_rows = []

    # Procesar los datos
    # Itera sobre cada línea de los datos
    for line in data.split("\n"):
        # Detecta la línea con el nombre del complejo
        if line.startswith("Complejo:"):
            # Si hay horarios almacenados, añade las filas correspondientes a data_rows
            if horarios:
                for hora in horarios:
                    data_rows.append({
                        "Fecha": date,
                        "Pais": country,
                        "Cine": "Multicinema",
                        "Nombre_cine": complejo.replace(" ", "_"),
                        "Titulo": titulo.replace(" ", "_"),
                        "Hora": hora,
                        "Idioma": idioma,
                        "Formato": formato
                    })
            #Extrae el nombre del complejo
            complejo = line.split("Complejo:")[1].strip()
            #Reinicia la lista de horarios
            horarios = []
        #Detecta la línea con el título de la película
        elif line.startswith("Título:"):
            #Extrae el título
            titulo = line.split("Título:")[1].strip()
        #Detecta la línea con la clasificación
        elif line.startswith("Clasificación:"):
            #Extrae la clasificación
            clasificacion = line.split("Clasificación:")[1].strip()
        #Detecta la línea con la promoción
        elif line.startswith("Promoción:"):
            #Extrae la promoción
            promocion = line.split("Promoción:")[1].strip()
        #Detecta la línea con la duración
        elif line.startswith("Duración:"):
            #Extrae la duración
            duracion = line.split("Duración:")[1].strip()
        #Detecta la línea con el idioma y formato
        elif line.startswith("Español"):
            #Si hay horarios almacenados, añade las filas correspondientes a data_rows
            if horarios:
                for hora in horarios:
                    data_rows.append({
                        "Fecha": date,
                        "Pais": country,
                        "Cine": "Multicinema",
                        "Nombre_cine": complejo.replace(" ", "_"),
                        "Titulo": titulo.replace(" ", "_"),
                        "Hora": hora,
                        "Idioma": idioma,
                        "Formato": formato
                    })
            #Separamos la línea en partes
            idioma_formato = line.strip().split()
            #El primer elemento de la cadena es el idioma
            idioma = idioma_formato[0]
            #La siguiente parte de la cadena es el formato(2D y 3D)
            formato = "".join(idioma_formato[1:]) if len(idioma_formato) > 1 else ""
            #Reinicia la lista de horarios
            horarios = []
        #Si la línea no está vacía
        elif line.strip():
             #Se añaden los horarios a la lista
            horarios.extend(line.strip().split())

    #Añadir las últimas filas correspondientes a data_rows
    if horarios:
        for hora in horarios:
            data_rows.append({
                "Fecha": date,
                "Pais": country,
                "Cine": "Multicinema",
                "Nombre_cine": complejo.replace(" ", "_"),
                "Titulo": titulo.replace(" ", "_"),
                "Hora": hora,
                "Idioma": idioma,
                "Formato": formato
            })
    #Devuelve las filas de datos
    return data_rows

#Función para combinar las partes de la hora
def combine_time_parts(data_rows):
    #Inicializar la lista para las filas combinadas
    combined_data = []
    # Variable para saltar la siguiente fila si se combinan partes de la hora
    skip_next = False

    for i in range(len(data_rows)):
        #Si la siguiente fila debe ser saltada
        if skip_next:
            skip_next = False
            continue
        
        # Obtener la fila actual
        current_row = data_rows[i]
        #Si la siguiente fila contiene AM o PM
        if i + 1 < len(data_rows) and data_rows[i+1]["Hora"] in ["AM", "PM"]:
            #Combina la hora con AM o PM
            current_row["Hora"] += " " + data_rows[i+1]["Hora"]
            #Marca que la siguiente fila debe ser saltada
            skip_next = True
        #Añadir la fila combinada a la lista
        combined_data.append(current_row)
        
    #Devuelve las filas combinadas
    return combined_data


if __name__=='__main__':
    #Crear instancia de Options
    options = Options()
    #Abrir la ventana del navegador en tamaño grande.
    options.add_argument('--start-maximized')
    #options.add_argument()

    driver_path = 'C:\\Users\\Usuario\\Desktop\\EdgeDriver\\msedgedriver.exe'
    service=Service(driver_path)
    driver = webdriver.Edge(service=service, options=options)
    driver.get('https://multicinema.com.sv/') 
    time.sleep(2)

    cartelera_button = driver.find_element(By.LINK_TEXT, "Cartelera")
    #Dar clic al botón "Cartelera" del navbar
    cartelera_button.click()

    #en la nueva página, en el selector elegimos "sabado 27 Julio 2024"
    # Encontrar el elemento select con el nombre "Dias"
    #select_element = driver.find_element(By.NAME, "Dias")

    # Crear un objeto Select para interactuar con el elemento
    #select_object = Select(select_element)

    # Seleccionar la opción por su texto visible
    #select_object.select_by_visible_text("Sabado 27  Julio  2024 ")

    #selector1 = driver.find_element(By.XPATH, '//*[@id="frmCartelera"]/div/center/select[1]/option[2]')
    #selector1.click()
    #selector2 = driver.find_element(By.XPATH, '//*[@id="frmCartelera"]/div/center/select[2]/option[2]')
    #selector2.click()
    #tambien seleccionamos Multicinema Plaza mundo soyapango
    #select_element2 = driver.find_element(By.NAME, "Complejo")
    #select_object2 = Select(select_element2)
    #select_object2.select_by_visible_text("Multicinema Plaza Mundo Soyapango")

    #Dar click al boton de consulta
    # Encontrar el botón "Consulta"
    #consulta_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Consulta']")
    # Hacer clic en el botón
    #consulta_button.click()
    time.sleep(2)
    #name_cinema=driver.find_element(By.XPATH, '//h3[@class="panel-title"]')
    #print(name_cinema.text[9:])
    # Cierra el navegador

    #obtener la fecha de la cartelera
    date_cinema=driver.find_element(By.XPATH, '/html/body/div[1]/div/div/h3/center')

    #variables para almacenar información
    #variable estatica, ya que el cine está ubicado en el mismo pais.
    country="El Salvador"
    #Array en el que se guardara la información a extraer.
    data_info=[]
    #seleccionar el div que contiene toda la información de la cartelera
    info_cinema=driver.find_elements(By.XPATH, '//div[@class="tab-content"]')
    for infos in info_cinema:
        data_info.append(infos.text)
        #data_info.append(infos.text)
        #print(infos.text)
    #unir los datos como una cadena, especificandoles un salto de linea.    
    data_info = "\n".join(data_info)
    #print(data_info)    
    #pasar los datos

    #convertir la fecha que se obtiene del sitio web, al formato mes-dia-año
    date_format=date_conversion(date_cinema)
    #estructurar los datos en filas.
    data_rows = cinema_data_analyzer(data_info, date_format, country)
    data_rows = combine_time_parts(data_rows)
    #crear el dataFrame 
    df=pd.DataFrame(data_rows)
    #df=df.to_string(index=False)
    print(df)
    #exportar el dataframe como un archivo de excel.
    df.to_excel('Multicinema2.xlsx', index=False)
    driver.quit()





            