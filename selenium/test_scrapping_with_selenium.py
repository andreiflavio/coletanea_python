# TODO - Instalar chromedriver - brew cask install chromedriver
# pip install selenium

# Útil: https://www.edureka.co/blog/web-scraping-with-python/
# Útil: https://selenium-python.readthedocs.io/api.html

# Implementar download dos mangás usando selenium
# baixando imagens, deverá gerar o pdf
import time
import requests

from selenium import webdriver
from bs4 import BeautifulSoup
    
driver = webdriver.Chrome("/usr/local/bin/chromedriver")
driver.get("https://unionleitor.top/leitor/Magi:_The_Labyrinth_of_Magic/224")

time.sleep(7)
page_source = driver.page_source

soup = BeautifulSoup(page_source, features="html.parser")
images = soup.find('div', attrs={'class':'col-sm-12 text-center'})
page = 0

for item in images.contents:
    if item != "\n":
        src = item.get("src")
        if src != "https://unionleitor.top/images/banner_scan.png" and \
            src!= "https://unionleitor.top/images/banner_forum.png":
            # abrir nova aba do driver
            driver.get(src)
            # simular ctrl + s
            driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 's')
            # selecionar uma pasta e salvar
            # fechar aba
            page += 1 
            print("Baixa imagem %s" % src)
driver.quit()
# Após salvar todas páginas, gerar pdf

# Tudo dando certo excluir respositório no github e criar um 
# novo intitulado exemplos em python.