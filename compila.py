import os,sys

from reportlab.lib.utils import ImageReader
from bollettino import Bollettino
from dataclasses import dataclass
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape, letter

#src = os.path.join(os.path.dirname(__file__),'bollettino.pdf')
from data import bollettino_pdf
# python -c "with open('bollettino.pdf', 'rb') as f: data = f.read() ; print('bollettino_pdf=',end='') ; print(data)" > data.py

LINE_HEIGHT = 16
BOXED_CHAR_SPACE = 4.75
@dataclass
class Field:
    x: int
    y: int
    rows: int = 1
    charSpace: float = 0
    padToRight: int = 0
    wrapAfter: int = None

    def draw(self, can: canvas, text:str):
        text = text.rjust(self.padToRight)
        if self.wrapAfter is None:
            lines = [text]
        else:
            lines = [ text[0:self.wrapAfter], text[self.wrapAfter:] ]
        y = self.y
        for l in lines:
            can.drawString(self.x, y, l, charSpace=self.charSpace)
            y-=LINE_HEIGHT

class BoxedField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.charSpace=BOXED_CHAR_SPACE


fields = {
    'Intestatario': [ Field(30,220, wrapAfter=34), BoxedField(392,220, wrapAfter=34) ],
    'Causale': [ Field(30,181), Field(392,179) ],
    'EseguitoDa': [ Field(30,140, wrapAfter=23), BoxedField(532,141, wrapAfter=23) ],
    'Via': [ Field(80,108), BoxedField(532,101) ],
    'Cap': [ Field(80,91), BoxedField(532,75) ],
    'Localita': [ Field(80,71), BoxedField(607,75) ],
    'ImportoCent': [ BoxedField(232,261, padToRight=10), BoxedField(699,261, padToRight=10) ],
    'ImportoInLettere': [ Field(105,247), Field(528,244) ],
    'ContoNumero': [ BoxedField(90,261, padToRight=8), BoxedField(468,261, padToRight=8) ]
}


PAGE_SIZE = landscape(A4)
def make_page(bollettino: Bollettino):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=PAGE_SIZE)
    #logo = ImageReader(io.BytesIO(logo_png))
    #can.drawImage(logo, 100,300, width=200, preserveAspectRatio=True)
    can.setFont('Courier', 13)
    for k,l in fields.items():
        val = bollettino.__getattribute__(k.lower())
        for f in l:
            f.draw(can, str(val))
    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    return new_pdf.getPage(0)

def compila(data: list[Bollettino], path:str, withSingles: bool, withPrint: bool, graphics:list[str]):
    # existing_pdf = PdfFileReader(open(src, "rb"))
    existing_pdf = PdfFileReader(io.BytesIO(bollettino_pdf))
    output = PdfFileWriter()
    page = existing_pdf.getPage(0)
    graphics_pdf = PdfFileWriter()
    graphics_pdf.addBlankPage(*PAGE_SIZE)
    graphics_page = graphics_pdf.getPage(0)
    for g in graphics:
        print(f"Carico {g}...")
        g_pdf = PdfFileReader(open(g, "rb"))
        graphics_page.mergePage(g_pdf.getPage(0))
    for bollettino in data:
        newpage = make_page(bollettino)
        newpage.mergePage(page)
        newpage.mergePage(graphics_page)
        output.addPage(newpage)
        if withSingles:
            output_single = PdfFileWriter()
            output_single.addPage(newpage)
            outputStream = open(os.path.join(path,f"{bollettino.eseguitoda}.pdf"), "wb")
            output_single.write(outputStream)
            outputStream.close()
    if withPrint:
        outputStream = open(os.path.join(path,"stampa.pdf"), "wb")
        output.write(outputStream)
        outputStream.close()
