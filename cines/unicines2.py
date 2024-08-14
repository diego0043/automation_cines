from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import locale
import pandas as pd
import re
from datetime import datetime

def formatear_fecha(fecha, anio):
    #se divide la fecha original en día y mes (en formato de texto)
    dia, mes_str = fecha.split('/')
    #se crea un objeto datetime con el día, mes y año proporcionados
    fecha_datetime = datetime.strptime(f"{dia}/{mes_str}/{anio}", "%d/%B/%Y")
    #se extrae el número del mes del objeto datetime
    mes_numero = fecha_datetime.month

    #Formateamos la fecha en el formato deseado (mes-día-año con mes en número)
    fecha_formateada = f"{mes_numero:02d}-{dia}-{anio}"
    #se retorna la fecha formateada
    return fecha_formateada


def extraer_idioma(lista_pelicula):
    #Se crea una lista vacía 'idiomas' para almacenar los idiomas encontrados.
    idiomas = []
    #la info de cada pelicula viene en una lista, se itera sobre está.
    for elemento in lista_pelicula:
        #se divide la lista apartir del salto de linea
        for parte in elemento.split("\n"):
            #si en la lista se encuentra la palabra "Dob" se agrega a la lista idiomas "Doblaje"
            if "Dob" in parte:
                idiomas.append("Doblaje")
                break
            elif "Sub" in parte:
                idiomas.append("Subtitulada")
                break
            elif "Inglés" in parte:
                idiomas.append("Inglés")
                break
    return idiomas

def extraer_horarios_completos(lista_pelicula):
    #Se crea una lista vacía para almacenar los horarios encontrados
  horarios = []
  #se itera sobre cada elemento (película) en la lista.
  for elemento in lista_pelicula:
    # Buscamos patrones de horarios más flexibles
    patron = r'\d{1,2}:\d{2}\s*[ap]m'  # Busca uno o dos dígitos(Hora), dos puntos, dos dígitos(minutos) y opcionalmente "am" o "pm"
    match = re.search(patron, elemento)
    #Si se encuentra una coincidencia, se agrega el horario a la lista
    if match:
      horarios.append(match.group())
  return horarios

#se encuentra el formato de la pelicula
def extraer_formato_pelicula(lista_pelicula):
    formato = []
    for elemento in lista_pelicula:
        for parte in elemento.split():
            if "2D" in parte:
                formato.append("2D")
                break
            elif "3D" in parte:
                formato.append("3D")
                break
                
    return formato


if __name__ == '__main__':
    #Crear instancia de Options
    options = Options()
    #Abrir la ventana del navegador en tamaño grande.
    options.add_argument('--start-maximized')
    #indicar la ruta local en la que se encuentra el driver
    driver_path = 'C:\\Users\\kevin\\OneDrive\\Escritorio\\Edge\\msedgedriver.exe'
    service=Service(driver_path)
    driver = webdriver.Edge(service=service, options=options)
    driver.get('https://unicines.com/cartelera.php') 
    time.sleep(2)
    
    # Localizar todos los enlaces dentro de la lista <ul id="cat_nav">
    enlaces = driver.find_elements(By.CSS_SELECTOR, "#cat_nav li a")
    # Recorrer cada enlace
    # Recorrer cada enlace por su índice
    #arreglo para almecenar data inicial
    data_info=[]

    for i in range(len(enlaces)):
        # Volver a encontrar los elementos <a> después de cada iteración para evitar StaleElementReferenceException
        enlaces = driver.find_elements(By.CSS_SELECTOR, "#cat_nav li a")
        
        # Obtener el href del enlace actual
        url = enlaces[i].get_attribute("href")
        
        # Navegar al enlace
        driver.get(url)
        
        #buscar el nombre del cine
        nombre_cine_completo=driver.find_elements(By.XPATH, '//h1[@class="nomargin_top"]')
        #buscar la información para cada pelicula
        info_cinema=driver.find_elements(By.XPATH, '//div[@class="strip_all_tour_list wow fadeIn"]')
        #buscar la fecha
        fecha_cartelera=driver.find_elements(By.XPATH, '//a[@class="accordion-toggle"]')

        #se obtiene el nombre del cine.
        for info_nombre_cine in nombre_cine_completo:
            nombre_cine=info_nombre_cine.text
        
        #se obtiene las peliculas en cartelera para cada cine y se le agrega el nombre del cine, la información se almacena en una lista.     
        for infos in info_cinema:
            info_cartelera=infos.text+ "\n" + nombre_cine[22:]
            data_info.append(info_cartelera)
        
        #se obtiene la fecha de la cartelera
        for info_fecha in fecha_cartelera:
            fecha_sin_formato=info_fecha.text
        
        # Pausa para ver el cambio de página (opcional)
        time.sleep(2)
        
        # Volver a la página principal
        driver.get("https://unicines.com/cartelera.php")

    #crear lista donde se almacenaran los elementos divididos por el salto de linea
    #esta lista sera la que se manipulara para obtener los datos que interesan para cada pelicula.
    new_data_info=[]
    data_rows=[] #lista que servira para almacenar los datos estructurados
    
    #bucle que recorre la información de la cartelera en general, para dividir la información de cada indice de la lista 
    #apartir del salto de linea.
    for i in data_info:
        data_string=i.split("\n")
        #En algunos casos las peliculas tiene la palabra "ESTRENO" como primer elemento de la lista,
        #este elemento se elimina porque no es necesario para la inforamción a obtener y queda como
        #primer elemento el nombre de la pelicula.
        if(data_string[0]=="ESTRENO"):
            data_string.pop(0)
        new_data_info.append(data_string)
    
    #llamamos a la función que da formato a la fecha, pasamos la fecha obtenida del sitio web, ya que este no tiene año
    #le pasamos el valor de 2024 para el año.
    fecha_formateada=formatear_fecha(fecha_sin_formato, 2024)
    
    #bucle para recorrer cada pelicula que se tiene en la lista y obtener los datos que interesan para cada pelicula
    for j in new_data_info:
        #llama la función que extrae los horarios para cada pelicula.
        horarios_completos=extraer_horarios_completos(j)
        #llama la función que extrae los formatos para cada pelicula
        formatos = extraer_formato_pelicula(j)
        #llama la función que extrae el idioma para cada pelicula. 
        idiomas = extraer_idioma(j)

        #se usa zip para iterar en conjunto sobre las listas que se obtuvieron al llamar las funciones anteriores
        #con está información se plantea construir una lista que contiene un diccionario con la información para cada pelicula
        for hora, formato, idioma in zip(horarios_completos, formatos, idiomas):
            data_rows.append({
                "Fecha": fecha_formateada,
                "Pais": "Honduras", #El cine opera solo en honduras, por lo que el valor se deja estatico.
                "Cine":"Unicines", #Nombre de cine es estatico, ya que es solo un cine.
                "Nombre cine":j[-1], #El nombre del cine se encuentra en la ultima posición de la lista de la información de cada pelicula.
                "Titulo":j[0], #El Titulo de la pélicula se encuentra en la primera posición de la lista de la información de cada pelicula.
                "Hora":hora,
                "Idioma": idioma,
                "Formato": formato 
            })

    #creamos el dataframe con la lista que contiene un diccionario por cada pelicula.
    df=pd.DataFrame(data_rows)
    #print(df)
    #se exporta el dataframe a archivo excel, se indica que no se requieren los indices del dataframe.
    df.to_excel('unicines.xlsx', index=False)

    # Cerrar el navegador
    driver.quit()
    