import os
import subprocess
from datetime import date

from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.lineplots import LinePlot

from reportlab.platypus.tableofcontents import TableOfContents

import PIL
import matplotlib.pyplot as plt

'''
product_filename = f'aurora'
product_version = '0_1_0'
docs_folderpath = f'C:/og-new/products/{product_filename}/{product_filename}_v{product_version}/docs'
'''

product_filename = f'aurora'
product_version = '0_1_0'
component_foldername = 'scheda_madre'
# docs_folderpath = f'C:/og-new/products/{product_filename}/{product_filename}__v{product_version}/{product_filename}__{component_foldername}__v{product_version}/docs'
docs_folderpath = f'C:/og-new/products/{product_filename}/{product_filename}__v{product_version}/docs'

input_folderpath = f'{docs_folderpath}/input'
output_folderpath = f'{docs_folderpath}/output'
prepared_for = "Staff Tecnico Interno"

### TODO: do the rest

cover_title_text = "Sistema Aurora"
cover_subtitle_text = "Piano Sviluppo"

# print()
# quit()
revision_history = []

################################################################################
# STYLES
################################################################################
styles = getSampleStyleSheet()
PRIMARY = colors.HexColor("#0B1F3B")
GREY = colors.HexColor("#6B7280")
LIGHT_GREY = colors.HexColor("#E5E7EB")
body_leading = 14
body_size = 9
body_space_after = 8
meta_style = ParagraphStyle(
    'meta', 
    fontSize=9, 
    textColor=GREY
)
cover_title_style = ParagraphStyle(
    'cover', 
    fontName='Helvetica-Bold', 
    fontSize=28, 
    leading=32, 
    textColor=PRIMARY
)
h1 = ParagraphStyle(
    'h1', 
    fontName='Helvetica-Bold', 
    fontSize=24, 
    leading=24,
    textColor=PRIMARY, 
    spaceBefore=0, 
    spaceAfter=body_leading
)
h2 = ParagraphStyle(
    'h2', 
    fontName='Helvetica-Bold', 
    fontSize=16, 
    leading=20,
    textColor=PRIMARY, 
    spaceBefore=0, 
    spaceAfter=body_leading
)
h3 = ParagraphStyle(
    'h3', 
    fontName='Helvetica-Bold', 
    fontSize=12, 
    textColor=PRIMARY, 
    spaceBefore=body_leading*1.5, 
    spaceAfter=body_leading
)
section_style = ParagraphStyle(
    'section', 
    fontName='Helvetica-Bold', 
    fontSize=16, 
    textColor=PRIMARY
)
body_style = ParagraphStyle(
    name="body_style",
    fontName="Helvetica",
    fontSize=10.5,
    leading=14.5,              # line spacing
    textColor=colors.HexColor("#222222"),
    alignment=0,               # left align
    spaceAfter=10,             # spacing between paragraphs
    spaceBefore=0,
    allowWidows=1,
    allowOrphans=0,
)
body_bold_style = ParagraphStyle(
    name="body_style",
    fontName="Helvetica-Bold",
    fontSize=10.5,
    leading=14.5,              # line spacing
    textColor=colors.HexColor("#222222"),
    alignment=0,               # left align
    spaceAfter=10,             # spacing between paragraphs
    spaceBefore=0,
    allowWidows=1,
    allowOrphans=0,
)
list_style = ParagraphStyle(
    name="list_style",
    fontName="Helvetica",
    fontSize=10.5,
    leading=14.5,              # spacing within lines
    textColor=colors.HexColor("#222222"),
    leftIndent=0,
    spaceAfter=0,
)
footer_style = ParagraphStyle(
    'footer', 
    fontSize=8,
    textColor=GREY, 
    alignment=TA_RIGHT
)

################################################################################
# COMPONENTS
################################################################################
class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)

        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="normal"
        )

        template = PageTemplate(
            id="main",
            frames=[frame],
            onPage=header_footer
        )
        self.addPageTemplates(template)

    def afterFlowable(self, flowable):

        if not isinstance(flowable, Paragraph):
            return
        
        style = flowable.style.name

        if style == "h1":
            level = 0
        elif style == "h2":
            level = 1
        elif style == "h3":
            level = 2
        else:
            return

        text = flowable.getPlainText()
        key = f"heading-{self.seq.nextf('heading')}"

        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(text, key, level)

        self.notify("TOCEntry", (level, text, self.page, key))

class AccentLine(Flowable):
    def draw(self):
        self.canv.setFillColor(PRIMARY)
        self.canv.rect(0, 0, 70, 4, fill=1, stroke=0)

def ul_gen(items):
    items_formatted = []
    for item in items:
        items_formatted.append(Paragraph(item, list_style))
    elements.append(
        ListFlowable(
            items_formatted,
            bulletType='bullet',
            leftIndent=12,
            bulletIndent=0,
            bulletFontName='Helvetica',
            bulletFontSize=8,
            bulletOffsetY=-2,
            spaceBefore=6,
            spaceAfter=12,
        )
    )

def ol_gen(items):
    items_formatted = []
    for item in items:
        items_formatted.append(Paragraph(item, list_style))
    elements.append(
        ListFlowable(
            items_formatted,
            bulletType='1',
            leftIndent=12,
            bulletIndent=0,
            bulletFontName='Helvetica',
            bulletFontSize=8,
            bulletOffsetY=-2,
            spaceBefore=6,
            spaceAfter=12,
        )
    )
    
def table_gen(items):
    table = Table(
        items,
        colWidths=[doc.width / len(items[0])] * len(items[0]),
    )
    table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),

        # Body
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#222222")),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),

        # Alternate row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
            [colors.white, colors.HexColor("#F8FAFC")]),

        # Borders
        ('LINEBELOW', (0, 0), (-1, 0), 1, PRIMARY),
        ('LINEBELOW', (0, 1), (-1, -1), 0.25, LIGHT_GREY),

        # Outer border
        ('BOX', (0, 0), (-1, -1), 0.5, LIGHT_GREY),

        # Alignment
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),   # Version
        ('ALIGN', (1, 0), (2, -1), 'CENTER'),   # Date, Author
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        # Left padding
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

################################################################################
# HEADER / FOOTER
################################################################################
def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LIGHT_GREY)
    canvas.line(70, 810, 525, 810)

    canvas.setFont("Helvetica", 8)
    canvas.drawString(70, 820, "OTREGROUP")
    canvas.drawRightString(525, 820, f"{date.today()}")

    canvas.drawString(70, 30, f"Confidenziale - V{product_version}")
    canvas.drawRightString(525, 30, str(doc.page))
    canvas.restoreState()

################################################################################
# PARSE
################################################################################
def parse(lines, elements):
    ul_start = False
    ul_items = []
    ol_start = False
    ol_items = []
    table_start = False
    table_items = []
    state = ''
    for line in lines:
        line = line.strip()
        line = line.replace('–', '-')
        line = line.replace('*', '')
        if line == '': continue

        if line == '[body]':  state = '[body]'
        elif line == '[/body]': state = ''

        if line.startswith('[') and line.endswith(']'): continue

        elif state == '[body]':
        
            if line.startswith('-----'):
                break
            
            if line.startswith('---'):
                if ul_start == True:
                    ul_start = False
                    ul_gen(ul_items)
                    ul_items = []
                if ol_start == True:
                    ol_start = False
                    ol_gen(ol_items)
                    ol_items = []
                if table_start == True:
                    table_start = False
                    table_gen(table_items)
                    table_items = []
                elements.append(PageBreak())
                continue
            
            if line.startswith('<spacer>'):
                elements.append(Spacer(1, 20))
                continue
            
            if line[0] == '-':
                line = line[1:].strip()
                ul_items.append(line)
                ul_start = True
                continue
            if ul_start == True:
                ul_start = False
                ul_gen(ul_items)
                ul_items = []
                
            if line[0].isdigit() and line[1] == '.':
                line = line[2:].strip()
                ol_items.append(line)
                ol_start = True
                continue
            if ol_start == True:
                ol_start = False
                ol_gen(ol_items)
                ol_items = []
                
            if line[0] == ':':
                line = line[1:].strip()
                row = [col.strip() for col in line.split(',')]
                table_items.append(row)
                table_start = True
                continue
            if table_start == True:
                table_start = False
                table_gen(table_items)
                table_items = []

            if line.startswith('###'):
                line = line.replace('###', '').strip()
                elements.append(Paragraph(line, h3))
            elif line.startswith('##'):
                line = line.replace('##', '').strip()
                elements.append(Paragraph(line, h2))
            elif line.startswith('#'):
                line = line.replace('#', '').strip()
                elements.append(Paragraph(line, h1))

            elif line.startswith('!'):
                line = line.split('(')[1].split(')')[0].split(' ')[0]
                print(line)
                # with PIL.Image.open(line) as img:
                #     width, height = img.size
                mul = 1.0
                # image_w = width * mul
                # image_h = height * mul
                target_width = 451.27
                target_width *= mul
                with PIL.Image.open(line) as im:
                    width, height = im.size
                scale = target_width / width
                image_w = width * scale
                image_h = height * scale  # SAME scale → keeps ratio

                img = Image(line, image_w, image_h)
                elements.append(Spacer(1, 10))
                img.hAlign = "CENTER"
                elements.append(img)
                elements.append(Spacer(1, 20))

            elif line.startswith('**'):
                line = line.replace('**', '').strip()
                # elements.append(Paragraph(line, body_bold_style))
                elements.append(Paragraph(line, body_style))
            else:
                line = line.strip()
                elements.append(Paragraph(line, body_style))
    if ul_start == True:
        ul_start = False
        ul_gen(ul_items)
        ul_items = []
    if lines:
        elements.append(PageBreak())

################################################################################
# CONTENT
################################################################################

def cover_add(elements):
    elements.append(Spacer(1, 100))
    elements.append(AccentLine())
    elements.append(Spacer(1, 25))
    elements.append(Paragraph(cover_title_text, cover_title_style))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(cover_subtitle_text, body_style))
    elements.append(Spacer(1, 100))
    elements.append(Paragraph("Documento preparato per", meta_style))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph(prepared_for, section_style))
    elements.append(Spacer(1, 60))
    if date.today().month == 1: month = 'Gennaio'
    if date.today().month == 2: month = 'Febbraio'
    if date.today().month == 3: month = 'Marzo'
    if date.today().month == 4: month = 'Aprile'
    if date.today().month == 5: month = 'Maggio'
    if date.today().month == 6: month = 'Giugno'
    if date.today().month == 7: month = 'Luglio'
    if date.today().month == 8: month = 'Agosto'
    if date.today().month == 9: month = 'Settembre'
    if date.today().month == 10: month = 'Ottobre'
    if date.today().month == 11: month = 'Novembre'
    if date.today().month == 12: month = 'Dicembre'
    elements.append(Paragraph(f"{month} {date.today().year}", meta_style))
    mul = 0.15
    image_w = 239 * mul
    image_h = 230 * mul
    img = Image(f"logo.png", image_w, image_h)
    elements.append(Spacer(1, 20))
    img.hAlign = "LEFT"
    elements.append(img)
    elements.append(Spacer(1, 120))
    elements.append(Paragraph("Non consentita la divulgazione", footer_style))
    elements.append(PageBreak())

# REV
# ------------------------------------------------------------------------------

def rev_parse(lines):
    for line in lines:
        line = line.strip()
        if line == '': continue

        if   line == '[rev]':  state = '[rev]'
        elif line == '[/rev]': state = '[/rev]'

        if line.startswith('[') and line.endswith(']'): continue

        if state == '[rev]':
            row = [col.strip() for col in line.split(',')]
            revision_history.append(row)

        elif state == '[/rev]': 
            break

def rev_add(elements):
    table = Table(
        revision_history,
        colWidths=[
            55,   # Version
            70,   # Date
            90,   # Author
            240,  # Description
        ],
    )
    table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),

        # Body
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#222222")),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),

        # Alternate row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
            [colors.white, colors.HexColor("#F8FAFC")]),

        # Borders
        ('LINEBELOW', (0, 0), (-1, 0), 1, PRIMARY),
        ('LINEBELOW', (0, 1), (-1, -1), 0.25, LIGHT_GREY),

        # Outer border
        ('BOX', (0, 0), (-1, -1), 0.5, LIGHT_GREY),

        # Alignment
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),   # Version
        ('ALIGN', (1, 0), (2, -1), 'CENTER'),   # Date, Author
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        # Left padding
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(Paragraph("Cronologia delle revisioni", h1))
    # elements.append(AccentLine())
    elements.append(Spacer(1, 10))
    elements.append(table)
    elements.append(PageBreak())

# TOC
# ------------------------------------------------------------------------------

def toc_add(elements):
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            "TOC1",
            fontName="Helvetica",
            fontSize=12,
            leftIndent=20,
            firstLineIndent=-20,
            spaceBefore=5,
        ),
        ParagraphStyle(
            "TOC2",
            fontName="Helvetica",
            fontSize=10,
            leftIndent=40,
            firstLineIndent=-20,
            spaceBefore=2,
        ),
        ParagraphStyle(
            "TOC3",
            fontName="Helvetica",
            fontSize=9,
            leftIndent=60,
            firstLineIndent=-20,
            spaceBefore=1,
        ),
    ]
    elements.append(Paragraph("Indice", h1))
    elements.append(toc)
    elements.append(PageBreak())

# BUILD
# ------------------------------------------------------------------------------

def run():
    elements = []

    input_filepath = f'output.md'
    output_filepath = f'output.pdf'
    with open(input_filepath, encoding='utf-8') as f: lines = f.read().split('\n')
    print(lines)

    ################################################################################
    # DOCUMENT SETUP
    ################################################################################
    doc = MyDocTemplate(
        output_filepath,
        pagesize=A4,
        rightMargin=70,
        leftMargin=70,
        topMargin=90,
        bottomMargin=60
    )

    cover_add(elements)
    rev_parse(lines)
    rev_add(elements)
    toc_add(elements)
    parse(lines, elements)
    
    # BUILD
    # doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
    doc.multiBuild(elements)

run()