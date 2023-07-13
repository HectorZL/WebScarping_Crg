import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = "http://lamansion-crg.net/forum/index.php"  # URL de la página
comment_selector = ".postcolor .post-entry a"  # Selector CSS para los enlaces del primer comentario

# Obtener el contenido HTML de la página
response = requests.get(url)
html = response.text

# Analizar el HTML con BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Encontrar el primer comentario y obtener todos los enlaces dentro de él
comment = soup.select(comment_selector)
links = [a["href"] for a in comment]

# Configurar Selenium para automatizar el navegador Brave
options = Options()
options.binary_location = '/bin/brave-browser'  
driver_path = '/path/to/chromedriver'  # Reemplaza esto con la ubicación real del archivo ejecutable del controlador de Chrome
driver = webdriver.Chrome(executable_path=driver_path, options=options)

# Abrir cada enlace en una ventana del navegador
for link in links:
    driver.get(link)

# Cerrar el navegador
driver.quit()

