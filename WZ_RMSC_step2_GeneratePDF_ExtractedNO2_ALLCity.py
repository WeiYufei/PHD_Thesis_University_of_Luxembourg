# coding=utf-8
from os import remove, listdir
from os.path import join
from reportlab.lib.pagesizes import A5, landscape, portrait
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileReader, PdfFileMerger

def get_jpgs(path):
    return [join(path, fn) for fn in listdir(path)
      if fn.endswith ('.jpg')]

jpg_files = get_jpgs(r'M:\RMSC_step2_SeperatePlots_ExtractedNO2_ALLCity')

result_pdf = PdfFileMerger()
temp_pdf = 'temp.pdf'


for fn in jpg_files:

    c = canvas.Canvas(temp_pdf, pagesize = landscape(A5))
    c.drawImage(fn, 0,0, *landscape(A5))
    c.save()
    
    with open(temp_pdf,'rb') as fp:
        pdf_reader = PdfFileReader(fp)
        result_pdf. append(pdf_reader)
###uncomment to generate pdf
#===============================================================================
# result_pdf.write('M://RMSC_step2_ExtractedNO2_ALLCity.pdf')
# result_pdf.close()
# remove(temp_pdf)
#===============================================================================
