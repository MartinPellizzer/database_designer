from reportlab.platypus import SimpleDocTemplate, Table
import re

from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.platypus import KeepTogether

# pdfmetrics.registerFont(
#     TTFont("DejaVuSans", "DejaVuSans.ttf")
# )

doc = SimpleDocTemplate("out.pdf")


style = ParagraphStyle(
    "table",
    fontName="Helvetica",
    fontSize=9,
    textColor="#475467",
    leading=11,
)

header_style = ParagraphStyle(
    "header",
    parent=style,
    fontName="Helvetica-Bold",
    textColor="#344054",
)

with open("output.md", encoding="utf-8") as f: md = f.read().strip()

def md_to_tables(md):
    md_elements = []
    md_element = ''

    for line in md.split('\n'):
        line = line.strip()
        if line.startswith('|'):
            md_element += line
            md_element += '\n'
        else:
            md_elements.append(md_element)
            md_element = ''

    if md_element != '':
        md_elements.append(md_element)

    return md_elements

md_elements = md_to_tables(md)


def markdown_table(md):
    rows = [
        [x.strip() for x in line.strip("|").split("|")]
        for line in md.splitlines()
        if line.strip() and not re.match(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$", line)
    ]

    rows = [
        [Paragraph(cell, header_style if i == 0 else style) for cell in row]
        for i, row in enumerate(rows)
    ]

    # table = Table(rows, colWidths=[doc.width / len(rows[0])] * len(rows[0]))
    table = Table(
        rows,
        colWidths=[doc.width * 0.2, doc.width * 0.8] 
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F2F4F7")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#344054")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#475467")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
        [colors.white, colors.HexColor("#FAFAFA")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    return table

elements_parse = []
for i, md_element in enumerate(md_elements):

    element_parse = markdown_table(md_element)

    table_elements = [element_parse]

    if i < len(md_elements) - 1:
        table_elements.append(Spacer(1, 40))

    elements_parse.append(KeepTogether(table_elements))

story = elements_parse

doc.build(story)