from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
from datetime import datetime

#funcion que sirve para obtener la fecha actual.
def date_conversion():
    fecha=datetime.now()
    fecha_formato=fecha.strftime("%m-%d-%Y")
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
        elif line.startswith("Español") or line.startswith("Subtitulada"):
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
    options = Options()
    options.add_argument('--start-maximized')
    driver_path = 'C:\\Users\\Usuario\\Desktop\\EdgeDriver\\msedgedriver.exe'
    service=Service(driver_path)
    driver = webdriver.Edge(service=service, options=options)
    driver.get('https://multicinema.com.sv/') 
    time.sleep(2)

    cartelera_button = driver.find_element(By.LINK_TEXT, "Cartelera")
    #Dar clic al botón "Cartelera" del navbar
    cartelera_button.click()
    time.sleep(2)

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

    #convertir la fecha que se obtiene del sitio web, al formato mes-dia-año
    date_format=date_conversion()
    #estructurar los datos en filas.
    data_rows = cinema_data_analyzer(data_info, date_format, country)
    data_rows = combine_time_parts(data_rows)
    #crear el dataFrame 
    df=pd.DataFrame(data_rows)
    #df=df.to_string(index=False)
    print(df)
    #exportar el dataframe como un archivo de excel.
    df.to_excel('Multicinema.xlsx', index=False)
    driver.quit()






            