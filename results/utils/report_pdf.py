from django.conf import settings
from reportlab.lib.pagesizes import A4, inch, landscape, portrait
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import HRFlowable, PageBreak, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab import platypus
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from os.path import exists
from core.models import Entity
from results.models import Period
from results.serializers import assessment
from results.utils.reports import wrap_aggr

BLACK_GRID = ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
VALIGN_MIDDLE = ('VALIGN', (0, 0), (-1, -1), 0.5, 'MIDDLE')
PADDING_2 = ('LEFTPADDING', (0, 0), (-1, -1), 2)
Story = [Spacer(1, 2 * inch)]


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
    file_exists = exists(image_path)
    if file_exists:
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

space = Spacer(0, 0.2 * inch)
hr = HRFlowable(width=560,
                thickness=2,
                color=colors.black,
                spaceBefore=10,
                spaceAfter=10)


def style_paragraph(data, p_style):
    return Paragraph(data, p_style)


def create_header(title=None):
    entity = Entity.objects.first()
    rows = [[
        get_image(f'{settings.MEDIA_ROOT}/{entity.logo}'),
        style_paragraph(entity.name.upper(), heading_style)
    ], ['', style_paragraph(entity.location, title_style)],
            ['', style_paragraph(entity.telephone, title_style)],
            ['', style_paragraph(entity.email, title_style)]]
    if title:
        rows.append(['', style_paragraph(title.upper(), heading_style2)])
    len_rows = len(rows)
    style = [('SPAN', (0, 0), (0, len_rows - 1)),
             ('LEFTPADDING', (0, 0), (0, len_rows - 1), 0)]
    table = Table(data=stretch_data(rows),
                  style=style,
                  colWidths=col_widths_by_ratio([1, 4]))
    return table


def create_student_table(student):
    class_room = student.class_room
    period = Period.objects.latest()
    if not student.picture:
        student.picture = 'profile-placeholder.png'
    image = get_image(f'{settings.MEDIA_ROOT}/{student.picture}')
    rows = [
        [image, 'Name', f'{student}', 'Period'],
        ['', 'Class', f'{class_room.name} {class_room.stream or ""}', ''],
        ['', 'DOB', f'{student.dob}', f'{period}'],
        ['', 'Sex', f'{student.gender}', ''],
    ]
    style = [('SPAN', (0, 0), (0, 3)), ('LEFTPADDING', (0, 0), (0, 3), 0),
             ('SPAN', (3, 0), (3, 1)), ('SPAN', (3, 2), (3, 3)),
             ('GRID', (1, 0), (-1, -1), 0.5, colors.black), VALIGN_MIDDLE]
    table = Table(data=stretch_data(rows),
                  style=style,
                  colWidths=col_widths_by_ratio([1.5, 1, 5, 1]))
    return table


def create_comment_table(computed_report):
    rows = [
        [
            'Class Teacher Comment',
            computed_report.report.class_teacher_comment
        ],
        ['Head Teacher Comment', computed_report.report.head_teacher_comment],
    ]
    style = [
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]
    table = Table(data=stretch_data(rows),
                  colWidths=col_widths_by_ratio([1, 3]),
                  style=style,
                  rowHeights=[40, 40])
    return table


class PDFReport:

    def __init__(self, computed_report, report_type, columns):
        self.computed_report = computed_report
        self.report_type = report_type
        self.columns = columns
        self.elements = []
        self.student = self.computed_report.student

    @property
    def title(self):
        level_group_name = self.student.class_room.level.level_group.name
        if self.report_type == 'assessment':
            report_type = 'TERMLY'
        else:
            report_type = 'COMPETENCY'
        return f'{level_group_name} - LEVEL, {report_type} REPORT'

    def create_elements(self):
        self.elements = []
        entity_table = self.create_entity_table()
        student_table = self.create_student_table()
        if self.report_type == 'assessment':
            body_table = self.create_body_table()
        else:
            body_table = self.create_activity_body_table()
        comment_table = self.create_comment_table()
        for element in [
                entity_table, hr, student_table, space, body_table, space
        ]:
            self.elements.append(element)
        if self.report_type == 'assessment':
            result_table = self.create_result_table()
            self.elements.append(result_table)
        self.elements.append(space)
        self.elements.append(comment_table)

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

    def create_entity_table(self):
        return create_header(title=self.title)

    def create_student_table(self):
        return create_student_table(self.computed_report.student)

    def create_body_table(self):
        return create_assessment_body_table(self.computed_report, self.columns)

    def create_comment_table(self):
        return create_comment_table(self.computed_report)

    def create_activity_body_table(self):
        return create_activity_body_table(self.computed_report, self.columns)

    def create_result_table(self):
        return create_result_table(self.computed_report,
                                   self.computed_report.student)


def create_activity_body_table(computed_report, columns):
    rows = []
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('LEFTPADDING', (0, 0), (-1, 0), 1),
    ]
    header = [col for col, available in columns.items() if available]
    # rows.append(header)

    subject_reports = computed_report.subject_reports

    row_index = 1
    for subject_report in subject_reports:
        subject = subject_report.subject
        activity_reports = subject_report.activities
        cols1 = [{
            'col': 'code',
            'name': 'code'
        }, {
            'col': 'subject',
            'name': 'name'
        }]
        cols2 = [{
            'col': 'competency',
            'name': 'name'
        }, {
            'col': 'mark',
            'name': 'mark'
        }, {
            'col': 'score',
            'name': 'score'
        }, {
            'col': 'descriptor',
            'name': 'descriptor'
        }]
        cols3 = [{
            'col': 'skills',
            'name': 'skills'
        }, {
            'col': 'remarks',
            'name': 'remarks'
        }, {
            'col': 'subjectTeacher',
            'name': 'subject_teacher_initials'
        }]
        row = []
        activity_len = len(activity_reports) or 1
        for col in cols1:
            if columns.get(col['col']):
                row.append(getattr(subject, col['name']))
                col_index = header.index(col['col'])
                style.append(('SPAN', (col_index, row_index),
                              (col_index, row_index + activity_len - 1)))

        try:
            activity1 = activity_reports[0]
            [
                row.append(getattr(activity1, col['name'])) for col in cols2
                if columns.get(col['col'])
            ]
        except IndexError:
            [row.append('') for col in cols2 if columns.get(col['col'])]

        for col in cols3:
            if columns.get(col['col']):
                row.append(getattr(subject_report, col['name']))
                col_index = header.index(col['col'])
                style.append(('SPAN', (col_index, row_index),
                              (col_index, row_index + activity_len - 1)))
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
    rows = [[col.upper() for col in header]] + rows
    style.append(('GRID', (0, 0), (-1, -1), 0.5, colors.black))
    ratios = calc_col_ratios(rows)
    col_widths = col_widths_by_ratio(ratios)
    table = Table(rows, style=style, colWidths=col_widths)
    table.vAlign = 'MIDDLE'
    return table


def create_assessment_body_table(computed_report, columns):
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


def insert_water_mark(canvas, doc):
    path = f'{settings.MEDIA_ROOT}mvara.png'
    canvas.saveState()
    canvas.drawImage(path, 120, 250, width=400, height=400, mask='auto')


class ScoresPDF:

    def __init__(self, scores_qs):
        self.scores_qs = scores_qs
        score = scores_qs.first()
        try:
            self.assessment = score.assessment
            self.title = Paragraph(f'Assessment: {self.assessment}',
                                   heading_style)
        except AttributeError:
            self.activity = score.activity
            self.title = Paragraph(f'Activity: {self.activity}', heading_style)

    def create_scores_table(self):
        rows = [[str(score.student), str(score.mark)]
                for score in self.scores_qs]
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
        doc = SimpleDocTemplate(f"{settings.MEDIA_ROOT}/scores.pdf",
                                pagesize=A4,
                                rightMargin=20,
                                leftMargin=20,
                                topMargin=20,
                                bottomMargin=20)
        doc.build(elements)
        return doc


class BulkPDFReport:

    def __init__(self, computed_reports, report_type, columns):
        self.computed_reports = computed_reports
        self.report_type = report_type
        self.columns = columns
        self.elements = []

    def create_elements(self):
        self.elements = []
        for computed_report in self.computed_reports:
            report = PDFReport(computed_report, self.report_type, self.columns)
            report.create_elements()
            self.elements += report.elements
            self.elements.append(PageBreak())
            # insert page break into elements

    def run(self):
        self.create_elements()
        doc = SimpleDocTemplate(f"{settings.MEDIA_ROOT}/class.pdf",
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


# class HorizontalRule(Flowable):
#     def __init__(self, width=3, strokecolor=colors.black):
#         self.width = width
#         self.strokecolor = strokecolor
#     def wrap(self, availWidth, availHeight):
#         self.availWidth = availWidth
#         return (availWidth, self.width + 2)
#     def draw(self):
#         canvas = self.canv
#         canvas.setLineWidth(self.width)
#         canvas.setStrokeColor(self.strokecolor)
#         p = canvas.beginPath()
#         p.moveTo(0, 1)
#         p.lineTo(self.availWidth, 1)
#         p.close()
#         canvas.drawPath( p )
