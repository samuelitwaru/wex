from reportlab.lib.pagesizes import A4, inch, landscape, portrait
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import HRFlowable, Paragraph, Spacer, Image
from reportlab.lib import colors
import os.path
from django.conf import  settings


BLACK_GRID = ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
VALIGN_MIDDLE = ('VALIGN', (0, 0), (-1, -1), 0.5, 'MIDDLE')
PADDING_2 = ('LEFTPADDING', (0, 0), (-1, -1), 2)
Story = [Spacer(1, 2 * inch)]


table_style = ParagraphStyle(name='table', fontSize=8, wordWrap=True)
heading_style = ParagraphStyle(name='heading',
                               fontSize=20,
                               wordWrap=True,
                               alignment=1,
                               padding=20)

heading_style2 = ParagraphStyle(name='heading',
                                fontSize=15,
                                wordWrap=True,
                                alignment=1,
                                padding=20)

title_style = ParagraphStyle(name='title',
                             fontSize=10,
                             wordWrap=True,
                             alignment=1)

space = Spacer(0, 0.1 * inch)

hr = HRFlowable(width=560,
                thickness=2,
                color=colors.black,
                spaceBefore=10,
                spaceAfter=10)

def style_paragraph(data, p_style):
    return Paragraph(data, p_style)

def calc_col_ratios(data):
    num_cols = len(data[0])
    ratios = []
    for i in range(num_cols):
        col = [row[i] for row in data]
        ratios.append(max([len(str(data)) for data in col]))
    return ratios


def stretch_data(data):
    return [[make_paragraph(cell, table_style) for cell in row]
            for row in data]


def make_paragraph(cell, style):
    try:
        return Paragraph(cell, style)
    except TypeError:
        return cell


def get_image(image_path, height=80):
    is_file = os.path.isfile(image_path)
    if is_file:
        image = Image(image_path)
        image.vAlign = 'CENTER'
        image.hAlign = 'CENTER'
        H = image.imageHeight
        W = image.imageWidth
        h = height
        w = h * (W / H)
        image.drawHeight = h
        image.drawWidth = w
        return image
    return ''


def col_widths_by_ratio(ratios, total_with=560):
    return [round((ratio / sum(ratios)) * total_with) for ratio in ratios]


def insert_water_mark(canvas, doc):
    path = f'{settings.MEDIA_ROOT}/mvara.png'
    canvas.saveState()
    canvas.drawImage(path, 120, 250, width=400, height=400, mask='auto')