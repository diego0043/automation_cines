from selenium.webdriver.support.ui import WebDriverWait
from config_selenium import *

# Abrir la página web
url='https://www.cinesmodernopanama.com/'
driver.get(url)

# Maximizar la ventana del navegador (opcional)
driver.maximize_window()

# Esperar unos segundos para asegurarse de que la página se cargue completamente (opcional)
time.sleep(2)

# Encontrar todos los elementos <a> que contienen enlaces a diferentes cines
wait=WebDriverWait(driver,10)
ham = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/header/a')))
ham.click()

elemento_menu = driver.find_element(By.XPATH, '//*[@id="cd-lateral-nav"]/ul[1]/li/a[@class="altura carteleraaltura"]')

elemento_menu.click()

sub_menu=wait.until(EC.visibility_of_element_located((By.XPATH,'//nav[@id="cd-lateral-nav"]//ul[@class="sub-menu"]')))

cines=sub_menu.find_elements(By.XPATH,'//a[contains(@id,"Semana_")]')
print(len(cines))
for option in cines:
    print(10*'-')
    option.click()
    combocomplejo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="cartelera"]/div/div[1]/div'))
    )
    NameCine=combocomplejo.find_element(By.CSS_SELECTOR,'.subtitulocomplejo').text
    print(NameCine)
    peliculas=combocomplejo.find_elements(By.XPATH,'//*[@id="cartelera"]/div/div[5]/div')
    for movie in peliculas:
        #print(movie.get_attribute('outerHTML'))
        print(10*'-')
        contenedorTitulo=movie.find_element(By.CSS_SELECTOR,'.combopelicartelera .combopelititulo')
        title=contenedorTitulo.find_element(By.TAG_NAME,'h2').text
        
        contenedorInfo=movie.find_element(By.CSS_SELECTOR,'.combodetallepeli .infopeli')
        language=contenedorInfo.find_element(By.CSS_SELECTOR,'.icosdetalle p').text
        
        print(f'Titulo: {title} Idioma: {language}')
        horarios_container = movie.find_element(By.CSS_SELECTOR, '.conjuntohorarios')
        horarios = horarios_container.find_elements(By.CSS_SELECTOR, '.horarioscartelera li.func-horario')

        for time in horarios:
            link_element = time.find_element(By.TAG_NAME, 'a')
            link_text = link_element.text
            try:
                hora, formato = link_text.split(' ')
                formato = formato.strip('()')
                print('Hora:', hora)  # Ejemplo de salida: 17:15
                print('Formato:', formato)  # Ejemplo de salida: 2D
            except ValueError:
                print("Error al dividir el texto:", link_text)
driver.quit()