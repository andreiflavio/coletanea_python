import os
import logging

from fpdf import FPDF

"""
    This script depends on to install ImageMagick.
    http://www.imagemagick.org/script/download.php#macosx
"""

files_errror = []
pdf = FPDF(orientation = 'P', format='A4')

def main(folder_with_files=None, filename="NewPDF"):
    files_errror.clear()
    create_pdf_from_png_files(folder_with_files, filename)
    if len(files_error) > 0:
        run_image_magick = input("There is some problems about pdf created.\
            Do you want to solve that problems (y/n)?")
        if run_image_magick == "y":
            # TODO - ler txt criado com arquivos que deram erro no nome
            # passar esses arquivos como parâmetro para método do imagemagick
            # rodar linha de comando via os.get_cwd para ajustar arquivos png
            main()

def create_pdf_from_png_files(folder_with_files, filename):
    count_files_folder = len(os.listdir(folder_with_files))
    for i in range(0, count_files_folder):
        path_file = folder_with_files + "/%d.png" % i
        try:
            pdf.add_page()
            pdf.image(path_file, w=185, h=237)
        except RuntimeError as ex:
            logging.error("Something wrong %s" % ex.args[0])
            # TODO - salvar num arquivo arquivos png que deram problema com de-interlacing
            files_error.append(path_file)
    pdf.output("%s/%s.pdf" % (folder_with_files, filename), "F") 

if __name__ == "__main__":
    # Informar diretório por parâmetros no CMD
    main("../webscraping/downloads/magi/224", "manga_224")