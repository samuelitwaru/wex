from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib import colors
from results.utils.reports import wrap_aggr
from core.models import Entity
from .utils import *
from .competency_report import create_comment_table, create_next_term_table


def create_header(title):
    entity = Entity.objects.first()
    rows = [
        [
            get_image(f'{settings.MEDIA_ROOT}/{entity.logo}'),
            style_paragraph(entity.name.upper(), heading_style)
        ], 
        ['', style_paragraph(entity.location, title_style)],
        ['', style_paragraph(entity.telephone, title_style)],
        ['', style_paragraph(entity.email, title_style)]
    ]
    
    style = [('SPAN', (0, 0), (0, -1)),
                ('BOTTOMPADDING', (1,0), (1,0), 10),
             ('LEFTPADDING', (0, 0), (0, -1), 0)]
    table = Table(data=stretch_data(rows),
                  style=style,
                  colWidths=col_widths_by_ratio([1, 4]))
    return table

def create_student_table(computed_report):
    student = computed_report.student
    if student.class_room.level.level_group.name == 'A':
        result = f'{computed_report.points} POINTS'
    else:
        result = f'{computed_report.aggregates} AGGREAGATES'
    class_room = student.class_room
    if not student.picture:
        student.picture = 'profile-placeholder.png'
    image = get_image(f'{settings.MEDIA_ROOT}/{student.picture}')
    rows = [
        [image, 'Name', f'{student}', 'Sex',f'{student.gender}', 'Result'],
        ['', 'Class', f'{class_room.name} {class_room.stream or ""}', 'Age',f'{student.age or "_"}', ''],
        ['', 'REG/NO', f'{student.index_no}', 'House',f'{student.house or ""}', result],
    ]
    style = [('SPAN', (0, 0), (0, 2)), ('LEFTPADDING', (0, 0), (0, 2), 0),
            #  ('SPAN', (3, 0), (3, 1)), ('SPAN', (3, 2), (3, 3)),
             ('GRID', (1, 0), (-1, -1), 0.5, colors.black), VALIGN_MIDDLE]
    table = Table(data=stretch_data(rows),
                  style=style,
                #   colWidths=col_widths_by_ratio([1.5, 1, 5, 2])
                )
    return table

def create_body_table(computed_report, columns):
    rows = []
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
    ]
    header = [col for col, available in columns.items() if available]
    # rows.append(header)

    subject_reports = computed_report.subject_reports

    row_index = 1
    for subject_report in subject_reports:
        subject = subject_report.subject
        paper_reports = subject_report.papers
        cols1 = [{
            'col': 'code',
            'name': 'code'
        }, {
            'col': 'subject',
            'name': 'name'
        }]
        cols2 = [{
            'col': 'paper',
            'name': 'description'
        }, {
            'col': 'assessments',
            'name': 'scores_string'
        }, {
            'col': 'score',
            'name': 'score'
        }, {
            'col': 'descriptor',
            'name': 'descriptor'
        }, {
            'col': 'total',
            'name': 'total'
        }, {
            'col': 'average',
            'name': 'average'
        }, {
            'col': 'aggregate',
            'name': 'aggregate'
        }]
        cols3 = [{
            'col': 'subjectAverage',
            'name': 'average'
        }, {
            'col': 'aggregates',
            'name': 'aggregate'
        }, {
            'col': 'grade',
            'name': 'letter_grade'
        }, {
            'col': 'points',
            'name': 'points'
        }, {
            'col': 'subjectTeacher',
            'name': 'subject_teacher_initials'
        }]
        row = []
        paper_len = len(paper_reports) or 1
        for col in cols1:
            if columns.get(col['col']):
                row.append(getattr(subject, col['name']))
                col_index = header.index(col['col'])
                style.append(('SPAN', (col_index, row_index),
                              (col_index, row_index + paper_len - 1)))

        try:
            paper1 = paper_reports[0]
            for col in cols2:
                if columns.get(col['col']):
                    data = getattr(paper1, col['name'])
                    if col['name'] == 'aggregate':
                        data = wrap_aggr(data)
                    row.append(str(data))
        except IndexError:
            [row.append('') for col in cols2 if columns.get(col['col'])]

        for col in cols3:
            if columns.get(col['col']):
                row.append(str(getattr(subject_report, col['name'])))
                col_index = header.index(col['col'])
                style.append(('SPAN', (col_index, row_index),
                              (col_index, row_index + paper_len - 1)))
        rows.append(row)
        row_index += paper_len

        for i in range(1, paper_len):
            span_row = []
            [span_row.append('') for col in cols1 if columns.get(col['col'])]
            activity = paper_reports[i]
            for col in cols2:
                if columns.get(col['col']):
                    data = getattr(activity, col['name'])
                    if col['name'] == 'aggregate':
                        data = wrap_aggr(data)
                    span_row.append(str(data))
            [span_row.append('') for col in cols3 if columns.get(col['col'])]
            rows.append(span_row)
    rows = [[col.upper() for col in header]] + rows
    style.append(BLACK_GRID)
    ratios = calc_col_ratios(rows)
    col_widths = col_widths_by_ratio(ratios)
    table = Table(rows, style=style, colWidths=col_widths)
    table.vAlign = 'MIDDLE'
    return table

def create_grading_system_table(grading_system):
    gs = grading_system
    rows = [
        ['D1', 'D2', 'C3', 'C4', 'C5', 'C6', 'P7', 'P8', 'F9'],
        list(
            map(
                lambda i: str(i+1),
                [gs.D2, gs.C3, gs.C4, gs.C5, gs.C6, gs.P7, gs.P8, gs.F9, -1]
            )
        )
    ]
    style = [BLACK_GRID]
    table = Table(data=stretch_data(rows), style=style, colWidths=col_widths_by_ratio([1]*9))
    return table

def create_result_table(computed_report, student):
    rows = [
        ['RESULT', ''],
    ]
    if student.class_room.level.level_group.name == 'A':
        rows.append(['POINTS', f'{computed_report.points} POINTS'])
    else:
        rows.append(
            ['AGGREGATES', f'{computed_report.aggregates} AGGREAGATES'])
    style = [BLACK_GRID, ('SPAN', (0, 0), (1, 0))]
    ratios = calc_col_ratios(rows)
    col_widths = col_widths_by_ratio(ratios)
    table = Table(rows, style=style, colWidths=col_widths)
    return table



class TermlyPDFReport:

    def __init__(self, computed_report, columns, grading_system, period):
        self.computed_report = computed_report
        self.columns = columns
        self.grading_system = grading_system
        self.period = period
        self.elements = []
        self.student = self.computed_report.student
        self.level_group = self.student.class_room.level.level_group
    
    @property
    def title(self):
        level_group_name = self.student.class_room.level.level_group.name
        return f'{level_group_name} - LEVEL, TERMLY REPORT, {self.period}'

    def create_elements(self):
        self.elements = []
        entity_table = create_header(self.title)
        title = style_paragraph(self.title.upper(), heading_style2)
        student_table = create_student_table(self.computed_report)
        body_table = create_body_table(self.computed_report, self.columns)
        gs_table = create_grading_system_table(self.grading_system)
        result_table = create_result_table(self.computed_report,
                                   self.computed_report.student)
        comment_table = create_comment_table(self.computed_report)
        next_term_table = create_next_term_table()

        for element in [
            entity_table, space, title, hr, student_table, space, body_table, space, gs_table,
            space, result_table, space, comment_table, space, next_term_table
        ]:
            self.elements.append(element)
    
    def run(self):
        self.create_elements()
        doc = SimpleDocTemplate(
            f"{settings.MEDIA_ROOT}/{self.computed_report.student.id}.pdf",
            pagesize=A4,
            rightMargin=20,
            leftMargin=20,
            topMargin=20,
            bottomMargin=20)
        doc.build(Story,
                  onFirstPage=insert_water_mark,
                  onLaterPages=insert_water_mark)
        doc.build(self.elements)
        return doc
