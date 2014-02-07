from lib.pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from lib.pdfminer.converter import TextConverter
from lib.pdfminer.layout import LAParams
from lib.pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

import os

def save_pdf(namefic):   
    fileitem = namefic
    if fileitem.filename:
        fn = os.path.basename(fileitem.filename)
        open('files/' + fn, 'wb').write(fileitem.file.read())
        message = 'The file "' + fn + '" was uploaded successfully'
    else:
        message = 'No file was uploaded'
       
    print """\
    Content-Type: text/html\n
    <html><body>
    <p>%s</p>
    </body></html>
    """ % (message)
    
def convert_pdf_to_txt(namefic):
    '''
    Convert pdf file to text
    :param namefic: is the name of file that we want to converte
    :return a string
    '''
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file("./datasetpdf/" + namefic + ".pdf", 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    fic = retstr.getvalue()
    retstr.close()

    return fic