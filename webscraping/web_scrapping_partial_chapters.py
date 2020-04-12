import os
import shutil
import datetime
import logging

import requests
from bs4 import BeautifulSoup
from fpdf import FPDF

# Criar Issue para os seguintes TODOs
# TODO - Adicionar regras deste arquivo no arquivo web_scraping.py - Demanda 
# mais testes para entender se há padrões. ESTE ARQUIVO SERÁ REMOVIDO NUM FUTURO PRÓXIMO

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info(datetime.datetime.now())
    base_path = "downloads/magi"

    try:
        os.mkdir(base_path)
    except:
        pass

    # 199 - 369
    url_manga = "https://unionleitor.top/leitor/Magi:_The_Labyrinth_of_Magic"
    chapter_start = 222
    chapter_end = 223
    generate_pdf_after_downloads = True
    pdf = None
    for chapter in range(chapter_start, chapter_end):
        logging.info("Chapter %d started" % (chapter))
        logging.info(datetime.datetime.now())

        url_request = '%s/%0.1f' % (url_manga, chapter + 0.5)
        response = requests.get(url_request, stream=True, 
            headers={'User-agent': 'Mozilla/5.0'})
        page = 0
        if generate_pdf_after_downloads:
            pdf = FPDF(orientation = 'P', format='A4')
        if response.status_code == 200:
            content = response.content
            soup = BeautifulSoup(content, features="html.parser")
            images = soup.find('div', attrs={'class':'col-sm-12 text-center'})
            for item in images.contents:
                if item != "\n":
                    src = item.get("src")
                    if src != "https://unionleitor.top/images/banner_scan.png" and \
                        src!= "https://unionleitor.top/images/banner_forum.png":
                        page += 1
                        path_file_formated = download_image(base_path, src, chapter, page)
                        if generate_pdf_after_downloads and path_file_formated:
                            pdf.add_page()
                            pdf.image(path_file_formated, w=185, h=237)
        logging.info("PDF generation of chapter %d started" % (chapter))
        if generate_pdf_after_downloads:
            pdf.output("%s/%0.1f.pdf" % (base_path, chapter + 0.5), "F")
        logging.info("PDF generation of chapter %d done" % (chapter))
        logging.info(datetime.datetime.now())
        logging.info("Chapter %d done" % (chapter))
    logging.info(datetime.datetime.now())


def download_image(base_path, url_image, chapter, page):
    response = requests.get(url_image,
                stream=True, headers={'User-agent': 'Mozilla/5.0'})
    type_file = url_image[len(url_image) - 3:len(url_image)]
    
    result = None
    try:
        url_formated = "%s/%0.1f" % (base_path, chapter + 0.5)
        os.mkdir(url_formated)
    except:
        pass
    if response.status_code == 200:
        path_file_formated = "%s/%s.%s" % (url_formated, page, type_file)
        with open(path_file_formated, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        logging.info("Page %d downloaded" % page)
        result = path_file_formated
    return result


if __name__ == "__main__":
    main()
