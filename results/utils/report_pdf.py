from django.conf import settings
from reportlab.lib.pagesizes import A4, inch, landscape, portrait
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors

'''
top_data
mid_data
bot_data
'''

def stretch_data(data):
	return [[make_paragraph(cell, table_style) for cell in row] for row in data]


def make_paragraph(cell, style):
    try:
        return Paragraph(cell,  style)
    except TypeError:
        return cell

def get_image(image_path):
	image = Image(image_path)
	H = image.imageHeight
	W = image.imageWidth
	h = 40
	w = h * (W/H)	
	image.drawHeight = h
	image.drawWidth = w
	return image

table_style = ParagraphStyle(name='table', fontSize=8, wordWrap=True)
heading_style = ParagraphStyle(name='heading', fontSize=10, wordWrap=True, alignment=1)

space = Spacer(0, 0.2*inch)


def create_pdf_report(computed_report):
    subject_reports = computed_report.subject_reports
    rows = []
    style = []
    row_span = 0
    for subj in subject_reports:
        row = []
        subject = subj.subject
        papers = subj.papers
        len_papers = len(papers) 
        style.append(('SPAN', (0,row_span), (0, row_span+len_papers-1)))
        style.append(('SPAN', (1,row_span), (1, row_span+len_papers-1)))
        style.append(('SPAN', (6,row_span), (6, row_span+len_papers-1)))
        style.append(('SPAN', (7,row_span), (7, row_span+len_papers-1)))
        style.append(('SPAN', (8,row_span), (8, row_span+len_papers-1)))
        style.append(('SPAN', (9,row_span), (9, row_span+len_papers-1)))
        row_span += len_papers
        row.append(subject.code)
        row.append(subject.name)
        row.append(subj.papers[0].paper.description)
        row.append(str(subj.papers[0].scores or ''))
        row.append(subj.papers[0].total)
        row.append(subj.papers[0].average)
        row.append(subj.average)
        row.append(subj.aggregate)
        row.append(subj.letter_grade)
        row.append(subj.points)
        rows.append(row)
        for i in range(1, len_papers):
            paper_report = papers[i]
            paper = paper_report.paper
            rows.append(
                ['','', paper.description, str(paper_report.scores or ''), paper_report.total, paper_report.average, '','','','']
                )
        # break
    style.append(('GRID', (0,0), (-1,-1), 0.5, colors.black))
    # rows = [['535', 'Physics', 'subj.papers', 0.0]]
    # style = []
    # style = [('SPAN', (0, 0), (0, 0)), ('SPAN', (1, 0), (1, 0)), ('SPAN', (3, 0), (3, 0))]
    print(rows)
    doc = SimpleDocTemplate(
		f"{settings.MEDIA_ROOT}/filename.pdf", pagesize=A4, rightMargin=20,
		leftMargin=20, topMargin=20, bottomMargin=20
    )
    table = Table(data=rows, style=style)
    elements = []
    elements.append(table)
    elements.append(space)
    elements.append(space)
    doc.build(elements)
    return rows    

