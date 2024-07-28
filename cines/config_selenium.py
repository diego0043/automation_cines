from datetime import date
import requests
import openpyxl
import datetime
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import time
import re

# Ruta al ejecutable de EdgeDriver ( especificar la ruta correcta )
path = 'C:/Users/ve180/Downloads/edgedriver_win64/msedgedriver.exe'

# Configurar las opciones de Edge
options = Options()
# Esta opción mantiene la pestaña abierta después de que el script termine
options.detach = True

# Configurar el servicio de EdgeDriver
service = Service(executable_path=path)

# Crear el driver de Edge con las opciones y el servicio configurados
driver = webdriver.Edge(service=service, options=options)