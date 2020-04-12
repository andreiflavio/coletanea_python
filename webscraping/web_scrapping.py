import os
import shutil
import datetime
import logging
import requests

from bs4 import BeautifulSoup
from fpdf import FPDF


# TODO - Resolver Issue #2 - Problema na geração do pdf do capítulo 224, 227, 229, 231.
# Ao mexer com esta Issue, tratar diretamente a pasta onde estão salvos os arquivos.
# Entender melhor o que seria interlacing

# TODO - Ler: https://www.scrapehero.com/how-to-prevent-getting-blacklisted-while-scraping/
# Ler: https://automatetheboringstuff.com/2e/chapter12/
# Ler: https://www.crummy.com/software/BeautifulSoup/

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
    chapter_start = 224
    chapter_end = 225
    generate_pdf_after_downloads = True
    pdf = None
    for chapter in range(chapter_start, chapter_end):
        logging.info("Chapter %d started" % (chapter))
        logging.info(datetime.datetime.now())

        url_request = '%s/%d' % (url_manga, chapter)
        response = requests.get(url_request, stream=True, 
            headers={'User-agent': 'Mozilla/5.0'})
        page = 0
        if response.status_code == 200:
            if generate_pdf_after_downloads:
                pdf = FPDF(orientation = 'P', format='A4')
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
                        try:
                            if generate_pdf_after_downloads and path_file_formated:
                                pdf.add_page()
                                pdf.image(path_file_formated, w=185, h=237)
                        except RuntimeError as ex:
                            logging.error("Something wrong when the page %d has been \
                                added in the pdf file." % page)
                            logging.error("It's a link about page: %s" % src)
                            logging.error("It's the error message: %s" % ex.args[0])
            logging.info("PDF generation of chapter %d started" % (chapter))
            if generate_pdf_after_downloads:
                pdf.output("%s/%d.pdf" % (base_path, chapter), "F")
            logging.info("PDF generation of chapter %d done" % (chapter))
            logging.info(datetime.datetime.now())
            logging.info("Chapter %d done" % (chapter))
        else:
            logging.error(response)              
    logging.info(datetime.datetime.now())


def download_image(base_path, url_image, chapter, page):
    response = requests.get(url_image,
                stream=True, headers={'User-agent': 'Mozilla/5.0'})
    type_file = url_image[len(url_image) - 3:len(url_image)]
    
    result = None
    try:
        url_formated = "%s/%s" % (base_path, chapter)
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
