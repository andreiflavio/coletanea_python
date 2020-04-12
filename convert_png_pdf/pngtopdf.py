import os
import logging

from fpdf import FPDF

"""
    This script depends on to install ImageMagick.
    http://www.imagemagick.org/script/download.php#macosx
"""
# TODO - Criar testes unitários

files_error = []
pdf = FPDF(orientation='P', format='A4')
logging.basicConfig(level=logging.INFO)


def main(folder_with_files=None, filename="NewPDF", type_file="png"):
    files_error.clear()
    create_pdf_from_png_files(folder_with_files, filename, type_file)
    if len(files_error) > 0:
        run_image_magick = input("There is some problems about pdf created.\
            Do you want to solve that problems (y/n)?")
        if run_image_magick == "y":
            logging.info("PDF will be recreated.")
            for item in files_error:
                os.system("convert -interlace none %s %s" % (item, item))
            main(folder_with_files, filename, type_file)


def create_pdf_from_png_files(folder_with_files, filename, type_file):
    count_files_folder = len(os.listdir(folder_with_files))
    for i in range(1, count_files_folder + 1):
        path_file = folder_with_files + "/%d.%s" % (i, type_file)
        # TODO - trocar este log info por um spinner
        logging.info("PNG %s file will be included on pdf file." % path_file)
        try:
            pdf.add_page()
            pdf.image(path_file, w=185, h=237)
        except RuntimeError as ex:
            logging.error("Something wrong %s" % ex.args[0])
            files_error.append(path_file)
    # pdf.output("%s/%s.pdf" % (folder_with_files, filename), "F")
    pdf.output("%s.pdf" % filename, "F")
    logging.info("PDF %s created" % filename)


if __name__ == "__main__":
    path = input("Where are png files?")
    filename = input("What is the name for pdf file you desired?")
    type_file = input("What is the type of images (PNG is default)?")
    main(path, filename, type_file)
