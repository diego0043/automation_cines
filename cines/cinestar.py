from config_selenium import *

driver.get('https://cinestar.com.gt/')

driver.maximize_window()

time.sleep(2)
country = "Guatemala"

carterlera = driver.find_element(By.XPATH, '//*[@id="menu-main-menu"]/li[2]/a')
carterlera.click()


time.sleep(2)

movies = driver.find_elements(By.CLASS_NAME, 'one-fourth')
anclas_by_movie = driver.find_element(By.XPATH, '//*[@id="padbody"]/div/div/div/div/div/div/div[1]/a')
                                                
len_movies_imitial = 1

for k in range(len(movies)):
    anclas_by_movie.click()
    time.sleep(2)
    len_movies_imitial = len_movies_imitial + 1;
    xpath_dina = '//*[@id="padbody"]/div/div/div/div/div/div/div['+str(len_movies_imitial)+']/a'
    driver.back()
    anclas_by_movie = driver.find_element(By.XPATH, xpath_dina)

    
