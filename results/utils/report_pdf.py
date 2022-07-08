from django.conf import settings
from reportlab.lib.pagesizes import A4, inch, landscape, portrait
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from os.path import exists
from core.models import Entity
from results.models import Period
from results.serializers import assessment


BLACK_GRID = ('GRID', (0,0), (-1,-1), 0.5, colors.black)
VALIGN_MIDDLE = ('VALIGN', (0,0), (-1,-1), 0.5, 'MIDDLE')
PADDING_2 = ('LEFTPADDING', (0,0), (-1,-1), 2)


def calc_col_ratios(data):
    num_cols = len(data[0])
    ratios = []
    for i in range(num_cols):
        col = [row[i] for row in data]
        ratios.append(max([len(str(data)) for data in col]))
    return ratios

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
        ('LEFTPADDING', (0,0), (0,3), 0)
        ]
    table = Table(
        data=stretch_data(rows), 
        style=style, colWidths=col_widths_by_ratio([1, 4]))
    return table

def create_student_table(student):
    class_room = student.class_room
    period = Period.objects.latest()
    if not student.picture:
        student.picture = 'profile-placeholder.png'
    image = get_image(f'{settings.MEDIA_ROOT}/{student.picture}')
    rows = [
        [image , 'Name',f'{student}','Period'],
        ['', 'Class', f'{class_room.name} {class_room.stream or ""}',''],
        ['', 'DOB', f'{student.dob}', f'{period}'],
        ['', 'Sex', f'{student.gender}',''],
    ]
    style = [
        ('SPAN', (0,0),(0,3)),
        ('LEFTPADDING', (0,0),(0,3), 0),
        ('SPAN', (3,0),(3,1)),
        ('SPAN', (3,2),(3,3)),
        ('GRID', (1,0), (-1,-1), 0.5, colors.black),
        VALIGN_MIDDLE
    ]
    table = Table(
        data=stretch_data(rows), 
        style=style, colWidths=col_widths_by_ratio([1.5,1,5,1])
        )
    return table



def create_comment_table(computed_report):
    rows = [
        ['Class Teacher Comment', computed_report.report.class_teacher_comment],
        ['Head Teacher Comment', computed_report.report.head_teacher_comment],

    ]
    style = [
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey ),
    ]
    table = Table(
        data=stretch_data(rows), colWidths=col_widths_by_ratio([1,3]), 
        style=style, rowHeights=[40,40])
    return table


def build_document(computed_report):
    doc = SimpleDocTemplate(
		f"{settings.MEDIA_ROOT}/{computed_report.student.id}.pdf", pagesize=A4, rightMargin=20,
		leftMargin=20, topMargin=20, bottomMargin=20
    )
    elements = []
    header_table = create_header()
    student_table = create_student_table(computed_report.student)
    # body_table = create_body_table(computed_report)
    comment_table = create_comment_table(computed_report)
    elements.append(header_table)
    elements.append(space)
    elements.append(student_table)
    elements.append(space)
    # elements.append(body_table)
    elements.append(space)
    elements.append(comment_table)
    doc.build(elements)
    return doc


class PDFReport:

    def __init__(self, computed_report, report_type, columns):
        self.computed_report = computed_report
        self.report_type = report_type
        self.columns = columns
    
    def run(self):
        entity_table = self.create_entity_table()
        student_table = self.create_student_table()
        if self.report_type == 'assessment':
            body_table = self.create_body_table()
        else:
            body_table = self.create_activity_body_table()
        comment_table = self.create_comment_table()
        doc = SimpleDocTemplate(
		f"{settings.MEDIA_ROOT}/{self.computed_report.student.id}.pdf", pagesize=A4, rightMargin=20,
		leftMargin=20, topMargin=20, bottomMargin=20)
        elements = []
        elements.append(entity_table)
        elements.append(space)
        elements.append(student_table)
        elements.append(space)
        elements.append(body_table)
        elements.append(space)
        if self.report_type == 'assessment':
            result_table = self.create_result_table()
            elements.append(result_table)
        elements.append(space)
        elements.append(comment_table)
        doc.build(elements)
        return doc

    def create_entity_table(self):
        return create_header()

    def create_student_table(self):
        return create_student_table(self.computed_report.student)

    def create_body_table(self):
        return create_assessment_body_table(self.computed_report, self.columns)

    def create_comment_table(self):
        return create_comment_table(self.computed_report)
    
    def create_activity_body_table(self):
        return create_activity_body_table(self.computed_report, self.columns)
    
    def create_result_table(self):
        return create_result_table(self.computed_report, self.computed_report.student)


def create_activity_body_table(computed_report, columns):
    rows = []
    style = []
    header = [col for col, available in columns.items() if available]
    rows.append(header)

    subject_reports = computed_report.subject_reports

    row_index = 1
    for subject_report in subject_reports:
        subject = subject_report.subject
        activity_reports = subject_report.activities
        cols1 = [{'col':'code', 'name':'code'}, {'col':'subject', 'name':'name'}]
        cols2 = [{'col':'competency', 'name':'name'}, {'col':'score', 'name':'score'}, {'col':'descriptor', 'name':'descriptor'}]
        cols3 = [{'col':'skills', 'name':'skills'}, {'col':'remarks', 'name':'remarks'}, {'col':'subjectTeacher', 'name':'subject_teacher_initials'}]
        row = []
        activity_len = len(activity_reports) or 1
        for col in cols1:
            if columns.get(col['col']):
                row.append(getattr(subject, col['name']))
                col_index = header.index(col['col'])
                style.append(('SPAN', (col_index, row_index), (col_index, row_index+activity_len-1)))
        
        try:
            activity1 = activity_reports[0]
            [row.append(getattr(activity1, col['name'])) for col in cols2 if columns.get(col['col'])]
        except IndexError:
            [row.append('') for col in cols2 if columns.get(col['col'])]
            
        for col in cols3:
            if columns.get(col['col']):
                row.append(getattr(subject_report, col['name']))
                col_index = header.index(col['col'])
                style.append(('SPAN', (col_index, row_index), (col_index, row_index+activity_len-1)))
        rows.append(row)
        row_index += activity_len
        
        for i in range(1, activity_len):
            span_row = []
            [span_row.append('') for col in cols1 if columns.get(col['col'])] 
            activity = activity_reports[i]
            for col in cols2:
                if columns.get(col['col']):
                    span_row.append(getattr(activity, col['name']))
            [span_row.append('') for col in cols3 if columns.get(col['col'])] 
            rows.append(span_row)

    style.append(('GRID', (0,0), (-1,-1), 0.5, colors.black))
    ratios = calc_col_ratios(rows)
    col_widths = col_widths_by_ratio(ratios)
    table = Table(rows, style=style, colWidths=col_widths)
    table.vAlign = 'MIDDLE'
    return table


def create_assessment_body_table(computed_report, columns):
    rows = []
    style = []
    header = [col for col, available in columns.items() if available]
    rows.append(header)

    subject_reports = computed_report.subject_reports

    row_index = 1
    for subject_report in subject_reports:
        subject = subject_report.subject
        paper_reports = subject_report.papers
        cols1 = [{'col':'code', 'name':'code'}, {'col':'subject', 'name':'name'}]
        cols2 = [{'col':'paper', 'name':'description'}, {'col':'assessments', 'name':'scores_string'}, {'col':'score', 'name':'score'}, {'col':'descriptor', 'name':'descriptor'}, {'col':'total', 'name':'total'}, {'col':'average', 'name':'average'}]
        cols3 = [
            {'col':'subjectAverage', 'name':'average'}, {'col':'aggregates', 'name':'aggregate'}, {'col':'grade', 'name':'letter_grade'}, 
            {'col':'points', 'name':'points'}, {'col':'subjectTeacher', 'name':'subject_teacher_initials'}]
        row = []
        paper_len = len(paper_reports) or 1
        for col in cols1:
            if columns.get(col['col']):
                row.append(getattr(subject, col['name']))
                col_index = header.index(col['col'])
                style.append(('SPAN', (col_index, row_index), (col_index, row_index+paper_len-1)))
        
        try:
            paper1 = paper_reports[0]            
            [row.append(str(getattr(paper1, col['name']))) for col in cols2 if columns.get(col['col'])]
        except IndexError:
            [row.append('') for col in cols2 if columns.get(col['col'])]
            
        for col in cols3:
            if columns.get(col['col']):
                row.append(str(getattr(subject_report, col['name'])))
                col_index = header.index(col['col'])
                style.append(('SPAN', (col_index, row_index), (col_index, row_index+paper_len-1)))
        rows.append(row)
        row_index += paper_len
        
        for i in range(1, paper_len):
            span_row = []
            [span_row.append('') for col in cols1 if columns.get(col['col'])] 
            activity = paper_reports[i]
            for col in cols2:
                if columns.get(col['col']):
                    span_row.append(str(getattr(activity, col['name'])))
            [span_row.append('') for col in cols3 if columns.get(col['col'])] 
            rows.append(span_row)
    style.append(BLACK_GRID)
    ratios = calc_col_ratios(rows)
    col_widths = col_widths_by_ratio(ratios)
    table = Table(rows, style=style, colWidths=col_widths)
    table.vAlign = 'MIDDLE'
    return table

def create_result_table(computed_report, student):
    rows = [
        ['RESULT', ''],
    ]
    if student.class_room.level.level_group.name == 'A':
        rows.append(['POINTS', f'{computed_report.points} POINTS'])
    else:
        rows.append(['AGGREGATES', f'{computed_report.aggregates} AGGREAGATES'])
    style = [BLACK_GRID, ('SPAN', (0,0), (1,0))]
    ratios = calc_col_ratios(rows)
    col_widths = col_widths_by_ratio(ratios)
    table = Table(rows, style=style, colWidths=col_widths)
    return table





class ScoresPDF:

    def __init__(self, scores_qs):
        self.scores_qs = scores_qs
        score = scores_qs.first()
        try:
            self.assessment = score.assessment
            self.title = Paragraph(f'Assessment: {self.assessment}', heading_style)
        except AttributeError:
            self.activity = score.activity
            self.title = Paragraph(f'Activity: {self.activity}', heading_style)

    def create_scores_table(self):
        rows = [[str(score.student), str(score.mark)] for score in self.scores_qs]
        style = [BLACK_GRID]
        ratios = calc_col_ratios(rows)
        col_widths = col_widths_by_ratio(ratios)
        table = Table(rows, style=style, colWidths=col_widths)
        return table
    
    def run(self):
        header_table = create_header()
        scores_table = self.create_scores_table()
        elements = []
        for el in [header_table, self.title, scores_table]:
            elements.append(el)
            elements.append(space)
        doc = SimpleDocTemplate(
		f"{settings.MEDIA_ROOT}/scores.pdf", pagesize=A4, rightMargin=20,
		leftMargin=20, topMargin=20, bottomMargin=20)
        doc.build(elements)
        return doc
