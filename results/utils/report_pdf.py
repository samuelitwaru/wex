from django.conf import settings
from reportlab.lib.pagesizes import A4, inch, landscape, portrait
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from os.path import exists
from core.models import Entity
from results.models import Period

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

def get_image(image_path, height=80):
    file_exists = exists(image_path)
    if file_exists:
        image = Image(image_path)
        image.vAlign = 'CENTER'
        image.hAlign = 'CENTER'
        H = image.imageHeight
        W = image.imageWidth
        h = height
        w = h * (W/H)	
        image.drawHeight = h
        image.drawWidth = w
        return image
    return ''

def col_widths_by_ratio(ratios, total_with=560):
    return [round((ratio/sum(ratios))*total_with) for ratio in ratios]
    

table_style = ParagraphStyle(name='table', fontSize=8, wordWrap=True)
heading_style = ParagraphStyle(name='heading', fontSize=15, wordWrap=True, alignment=1, padding=20)
title_style = ParagraphStyle(name='title', fontSize=10, wordWrap=True, alignment=1)

space = Spacer(0, 0.2*inch)

def style_paragraph(data, p_style):
    return Paragraph(data, p_style)



def create_header():
    entity = Entity.objects.first()
    rows = [
        [get_image(f'{settings.MEDIA_ROOT}/{entity.logo}'), style_paragraph(entity.name, heading_style)],
        ['', style_paragraph(entity.location, title_style)],
        ['',  style_paragraph(entity.telephone, title_style)],
        ['',  style_paragraph(entity.email, title_style)]
    ]
    style = [
        ('SPAN', (0,0), (0,3)), 
        ('GRID', (0,0), (0,3), 0.5, colors.grey)
        ]
    table = Table(data=stretch_data(rows), style=style, colWidths=col_widths_by_ratio([1, 3.8]))
    return table

def create_student_table(student):
    class_room = student.class_room
    period = Period.objects.latest()
    if not student.picture:
        student.picture = 'profile-placeholder.png'
    image = get_image(f'{settings.MEDIA_ROOT}/{student.picture}')
    rows = [
        [image ,f'{student}','Period'],
        ['',f'{class_room.name} {class_room.stream or ""}',''],
        ['',f'{student.dob}', f'{period}'],
        ['',f'{student.gender}',''],
    ]
    style = [
        ('SPAN', (0,0),(0,3)),
        ('SPAN', (2,0),(2,1)),
        ('SPAN', (2,2),(2,3)),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]
    table = Table(
        data=stretch_data(rows), 
        style=style, colWidths=col_widths_by_ratio([1,4,1])
        )
    return table



def create_comment_table(computed_report):
    rows = [
        ['Class Teacher Comment', computed_report.report.class_teacher_comment],
        ['Class Teacher Comment', computed_report.report.head_teacher_comment],

    ]
    style = [
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey )
    ]
    table = Table(
        data=stretch_data(rows), colWidths=col_widths_by_ratio([1,3]), 
        style=style)
    return table


def create_body_table(computed_report):
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
        papers = subj.papers
        if len(papers):
            row.append(papers[0].paper.description)
            row.append(str(papers[0].scores or ''))
            row.append(str(papers[0].total))
            row.append(str(papers[0].average))
        else:
            [row.append('') for i in range(0,4)]
        row.append(str(subj.average))
        row.append(str(subj.aggregate))
        row.append(subj.letter_grade)
        row.append(str(subj.points))
        rows.append(row)
        for i in range(1, len_papers):
            paper_report = papers[i]
            paper = paper_report.paper
            rows.append(
                ['','', paper.description, str(paper_report.scores or ''), str(paper_report.total), str(paper_report.average), '','','','']
                )
    style.append(('GRID', (0,0), (-1,-1), 0.5, colors.black))
    num_cols = len(rows[0])
    table = Table(
        data=stretch_data(rows), 
        style=style, colWidths=col_widths_by_ratio([1]*num_cols)
    )
    return table


def build_document(computed_report):
    doc = SimpleDocTemplate(
		f"{settings.MEDIA_ROOT}/{computed_report.student.id}.pdf", pagesize=A4, rightMargin=20,
		leftMargin=20, topMargin=20, bottomMargin=20
    )
    elements = []
    header_table = create_header()
    student_table = create_student_table(computed_report.student)
    body_table = create_body_table(computed_report)
    comment_table = create_comment_table(computed_report)
    elements.append(header_table)
    elements.append(space)
    elements.append(student_table)
    elements.append(space)
    elements.append(body_table)
    elements.append(space)
    elements.append(comment_table)
    doc.build(elements)
    return doc

