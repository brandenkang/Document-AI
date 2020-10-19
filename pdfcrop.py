import PyPDF2
# import pyPdf
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from PIL import Image
from PIL import ImageEnhance


def extract_tree(in_file, out_file):
    with open(in_file, 'rb') as infp:
        # Read the document that contains the tree (in its first page)
        reader = PyPDF2.PdfFileReader(infp)
        page = reader.getPage(0)

        # Crop the tree. Coordinates below are only referential
        page.cropBox.lowerLeft = [5,50]
        page.cropBox.upperRight = [310,1000]

        # Create an empty document and add a single page containing only the cropped page
        writer = PyPDF2.PdfFileWriter()
        writer.addPage(page)
        with open(out_file, 'wb') as outfp:   
            writer.write(outfp)


# First, crop the tree and save it into cropped_document.pdf
extract_tree('/Users/BrandenKang/Document-AI/DB_before_crop.pdf', 'trial_999.pdf')

# def get_enhanced_pdf(): 
#     image = convert_from_path('trial_1.pdf')
#     for img in image: 
#         # enhancer_object = ImageEnhance.Contrast(img)
#         # out = enhancer_object.enhance(2.0)
#         # out = ImageEnhance.Sharpness(out)
#         # out = out.enhance(2.0)

#         enhancer_object = ImageEnhance.Sharpness(img)
#         out = enhancer_object.enhance(1.8)
#         out.save('trial_11.pdf','PDF')

# get_enhanced_pdf()










# with open('2.pdf','rb') as fin:
#     pdf = PyPDF2.PdfFileReader(fin)
#     page = pdf.getPage(0)

#     # Coordinates found by inspection.
#     # Can these coordinates be found automatically?
#     page.cropBox.lowerLeft=(88,322)
#     page.cropBox.upperRight = (508,602)

#     output = PyPDF2.PdfFileWriter()
#     output.addPage(page)

#     with open('cropped-5.pdf','wb') as fo:
#         output.write(fo)


# ----------------------------------------------------------------------------------------------------------------------------- # 

# Now merge document2.pdf with cropped_document.pdf
# insert_tree_into_page('cropped_document.pdf', 'document2.pdf')


# from pathlib import Path
# from PyPDF2 import PdfFileReader, PdfFileWriter

# pdf_path = (
#     Path.home()
#     /"Document-AI/sample.pdf"
#     # "sample.pdf"
# )

# pdf_reader = PdfFileReader(str(pdf_path))
# first_page = pdf_reader.getPage(0)

# print(first_page.mediaBox)
