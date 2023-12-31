# -*- coding: utf-8 -*-
"""update Scanned_pdf_to_text.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cSOzwNdQyfq6qxnyMqnnYWtuDfgsd2RH
"""

"""
install these packages
  
  pip install PyPDF2  
  pip install pdf2image
  pip install pytesseract
  sudo apt-get install poppler-utils
  sudo apt install tesseract-ocr
________________________________________________________________

There are two parts to the program as follows:

Part #1: 
Deals with converting the PDF into image files. Each page of the PDF is stored as an image file. 
The names of the images stored are: 
      PDF page 1 -> im1.jpg PDF page 2 -> im2.jpg PDF page 3 -> im3.jpg …. PDF page n -> imn.jpg.

Part #2: 
Deals with recognizing text from the image files and storing it into a text file
________________________________________________________________________________________________________________
Advantages of this method include:

* Avoiding text-based conversion because of the encoding scheme resulting in loss of data.
* Even handwritten content in PDF can be recognized due to the usage of OCR.
* Recognizing only particular pages of the PDF is also possible.
* Getting the text as a variable so that any amount of required pre-processing can be done.
______________________________________________________________________________________________________________________
Disadvantages of this method include:

* Disk storage is used to store the images in the local system. Although these images are tiny in size.
* Using OCR cannot guarantee 100% accuracy. Given a computer-typed PDF document results in very high accuracy.
* Handwritten PDFs are still recognized, but the accuracy depends on various factors like handwriting, page color, etc.

"""

import pytesseract
from PIL import Image
import PyPDF2
import os
from pytesseract import image_to_string
from pdf2image import convert_from_path
from PyPDF2 import PdfReader

# simple pdf text extracter function. you just pass pdf file path and empty_txt_file_path. 
# empty_txt_file_path must be the path of empty txt file 

def simple_PDF_extractor(pdf_path, empty_txt_file_path):
  # Open the PDF file
  with open(pdf_path, "rb") as file:
      # Create a PDF reader object
      reader = PyPDF2.PdfReader(file)

     # Iterate over each page in the PDF
      for page in range(len(reader.pages)):
          # Extract the text from the page
          text = reader.pages[page].extract_text()

          #create empyty text file name < sample.txt >
          text_file = open(empty_txt_file_path, "a+")
          # write extracted text into this file
          n = text_file.write(text+"\n")
          print(text)
          # close file
      text_file.close()


# scanned pdf text extracter function. you just pass pdf path and empty_txt_file_path as a parameter 
# then it will extract all the text the given empty file.

def scanned_pdf_extractor(pdf_path,empty_txt_file_path):
# Open the PDF file
  # Open the PDF file
 with open('/content/book7.pdf', 'rb') as pdf_file:
     pdf_reader = PdfReader(pdf_file)
     image_file_list = []
     # Iterate over each page
     for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        # Extract the image data
        xObject = page['/Resources']['/XObject'].get_object()
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].get_data()
                filename=obj[1:] + ".jpg"
                img = open(filename, "wb")
                img.write(data)
                img.close()
                image_file_list.append(filename)
        image_file_list=image_file_list[:6]

      # recognize text from images and store in text file
 with open(empty_txt_file_path, "w") as f:
        for i,page in enumerate(image_file_list):
             text = image_to_string(page)
             f.write("page {}: {}\n".format(i+1, text))
        #text = image_to_string(image_file_list[len(image_file_list)-1])
        #f.write(text)
                


# simple_pdf_extractor function called 
# Give the path of a pdf and file_save_path  as a parameter 

pdf_path="/content/7743-Article Text-13981-1-10-20210530.pdf"
empty_txt_file_path="/content/sample_data/simple.txt"

simple_PDF_extractor(pdf_path,empty_txt_file_path)


# scanned_pdf_extractor function called
pdf_file_path="/content/book7.pdf"
empty_txt_file_path="/content/sample_data/output.txt"
scanned_pdf_extractor(pdf_file_path, empty_txt_file_path)