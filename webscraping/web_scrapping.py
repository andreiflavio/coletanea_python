import os
import shutil
import datetime
import logging
import requests

from bs4 import BeautifulSoup
from fpdf import FPDF

""""
    If you want, that script able to use together with pngtopdf.py
"""

# TODO - Ler: https://www.scrapehero.com/how-to-prevent-getting-blacklisted-while-scraping/
# Ler: https://automatetheboringstuff.com/2e/chapter12/
# Ler: https://www.crummy.com/software/BeautifulSoup/


def main(chapter_start, chapter_end, generate_pdf_after_downloads):
    logging.basicConfig(level=logging.INFO)
    logging.info(datetime.datetime.now())
    base_path = "downloads/magi"

    try:
        os.mkdir(base_path)
    except:
        pass

    # Lido 199 - 223
    # A Baixar 249 - 369
    url_manga = "https://unionleitor.top/leitor/Magi:_The_Labyrinth_of_Magic"
    pdf = None
    chapters_error_pdf = []
    for chapter in range(chapter_start, chapter_end):
        logging.info("Chapter %d started" % (chapter))
        logging.info(datetime.datetime.now())

        url_request = '%s/%d' % (url_manga, chapter)
        response = requests.get(url_request, stream=True, 
                                headers={'User-agent': 'Mozilla/5.0'})
        page = 0
        if response.status_code == 200:
            if generate_pdf_after_downloads:
                pdf = FPDF(orientation='P', format='A4')
            content = response.content
            soup = BeautifulSoup(content, features="html.parser")
            images = soup.find('div', attrs={'class':'col-sm-12 text-center'})
            for item in images.contents:
                if item != "\n":
                    src = item.get("src")
                    if must_ignored(src):
                        page += 1
                        path_file_formated = download_image(
                            base_path, src, chapter, page)
                        try:
                            if generate_pdf_after_downloads and \
                                path_file_formated:
                                pdf.add_page()
                                pdf.image(path_file_formated, w=185, h=237)
                        except RuntimeError as ex:
                            logging.error("Something wrong when the page %d has been \
                                added in the pdf file." % page)
                            logging.error("It's a link about page: %s" % src)
                            logging.error("It's the error message: %s" % ex.args[0])
                            chapters_error_pdf.append("%s\n" % path_file_formated)
            if generate_pdf_after_downloads and len(chapters_error_pdf) <= 0:
                logging.info("PDF generation of chapter %d started" % (chapter))
                pdf.output("%s/%d.pdf" % (base_path, chapter), "F")
                logging.info("PDF generation of chapter %d done" % (chapter))
            if len(chapters_error_pdf) > 0:
                create_txt_about_errors(chapters_error_pdf)
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


def create_txt_about_errors(chapters_error_pdf):
    txt_error = open("%s_error.txt" % datetime.datetime.now(), "w")
    txt_error.writelines(chapters_error_pdf)
    txt_error.close()


def must_ignored(src):
    result = src != "https://unionleitor.top/images/banner_scan.png" and \
        src!= "https://unionleitor.top/images/banner_forum.png"
    return result


if __name__ == "__main__":
    chapter_start = input("What chapter would you like to start download: ")
    chapter_end = input("What chapter would you like to end download: ")
    generate_pdf_after_downloads = input("Would you like to create a pdf file\
        for each chapter (this process is expensive) (y/n)")
    main(int(chapter_start), int(chapter_end) + 1,
        generate_pdf_after_downloads == "y")
