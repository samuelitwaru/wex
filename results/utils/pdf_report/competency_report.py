from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib import colors
from core.models import Entity, Profile
from django.contrib.auth.models import User
from .utils import *


def create_header():
    entity = Entity.objects.first()
    rows = [
        [
            get_image(f'{settings.MEDIA_ROOT}/{entity.logo}'), style_paragraph(entity.name.upper(), heading_style)
        ], 
        ['', style_paragraph(entity.location, title_style)],
        ['', style_paragraph(entity.telephone, title_style)],
        ['', style_paragraph(entity.email, title_style)]
    ]

    style = [
            ('SPAN', (0, 0), (0,  -1)), 
            ('BOTTOMPADDING', (1,0), (1,0), 10),
            ('LEFTPADDING', (0, 0), (0, -1), 0)
        ]

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
             ('GRID', (1, 0), (-1, -1), 0.5, colors.black), VALIGN_MIDDLE]
    table = Table(data=stretch_data(rows),
                  style=style,
                )
    return table


def create_activity_body_table(computed_report, columns):
    rows = []
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('LEFTPADDING', (0, 0), (-1, 0), 1),
    ]
    header = [col for col, available in columns.items() if available]

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
            'col': 'totalScores',
            'name': 'scores_string'
        }, {
            'col': 'average',
            'name': 'activity_average_score'
        }, {
            'col': 'identifier',
            'name': 'activity_score'
        }, {
            'col': 'achievement',
            'name': 'activity_score_identifier',
        }, {
            'col': 'initials',
            'name': 'subject_teacher_initials',
        }]
        row = []
        for col in cols1:
            if columns.get(col['col']):
                row.append(getattr(subject, col['name']))
        for col in cols2:
            if columns.get(col['col']):
                row.append(getattr(subject_report, col['name']))
        rows.append(row)
    rows = [[col.upper() for col in header]] + rows
    style.append(('GRID', (0, 0), (-1, -1), 0.5, colors.black))
    ratios = calc_col_ratios(rows)
    col_widths = col_widths_by_ratio(ratios)
    table = Table(rows, style=style, colWidths=col_widths)
    table.vAlign = 'MIDDLE'
    return table


def create_competency_result_table(computed_report):
    rows = [
       ['Total',f'{computed_report.total_scores}','Average',f'{round(computed_report.average_scores, 2)}']
    ]
    style = [
        BLACK_GRID
    ]
    # ratios = calc_col_ratios(rows)
    table = Table(data=stretch_data(rows),
                  colWidths=col_widths_by_ratio([3,1,3,1]),
                  style=style
                  )
    return table


def create_comment_table(computed_report):
    ht_signature = ''
    ct_signature = ''
    head_teacher = User.objects.filter(groups__name__in=['head_teacher']).first()
    class_teacher = computed_report.student.class_room.teacher.user
    if head_teacher:
        ht_profile, created = Profile.objects.get_or_create(user=head_teacher)
        ht_signature = get_image(f'{settings.MEDIA_ROOT}/{ht_profile.signature}', height=35)
    if class_teacher:
        ct_profile, created = Profile.objects.get_or_create(user=class_teacher)
        ct_signature = get_image(f'{settings.MEDIA_ROOT}/{ct_profile.signature}', height=35)
    rows = [
        ['Class Teacher Comment', 'Signature'],
        [computed_report.report.class_teacher_comment,ct_signature],
        ['',''],
        ['Head Teacher Comment', 'Signature'],
        [computed_report.report.head_teacher_comment,ht_signature],
    ]
    style = [
        ('GRID', (0, 0), (-1, 1), 0.5, colors.grey),
        ('GRID', (0, 3), (-1, -1), 0.5, colors.grey),
    ]
    table = Table(data=stretch_data(rows),
                  colWidths=col_widths_by_ratio([3, 1]),
                  style=style,
                  rowHeights=[20, 40, 5, 20, 40])
    return table


def create_next_term_table():
    rows = [
        ['Next term starts: ', 'Next term ends: '],
    ]
    style = [
        BLACK_GRID
    ]
    table = Table(data=stretch_data(rows),
                  colWidths=col_widths_by_ratio([1, 1]),
                  style=style
                  )
    return table


def create_score_key_table():
    rows = [
        ['Identifier: ', 'Achievement', 'Descriptor'],
        ['1', 'Basic', 'Some learning outcomes achieved but not sufficient for overall achievement'],
        ['2', 'Moderate', 'Most learning outcomes achieved enough for overall achiement'],
        ['3', 'Outstading', 'All learning outcomes achieved with care'],
    ]
    style = [
        BLACK_GRID
    ]
    ratios = calc_col_ratios(rows)
    table = Table(data=stretch_data(rows),
                  colWidths=col_widths_by_ratio(ratios),
                  style=style
                  )
    return table


def create_result_table(computed_report):
    rows = [
       ['Total',f'{computed_report.total_scores}','Average',f'{round(computed_report.average_scores, 2)}']
    ]
    style = [
        BLACK_GRID
    ]
    # ratios = calc_col_ratios(rows)
    table = Table(data=stretch_data(rows),
                  colWidths=col_widths_by_ratio([3,1,3,1]),
                  style=style
                  )
    return table


class CompetencePDFReport:

    def __init__(self, computed_report, columns, grading_system, period):
        self.computed_report = computed_report
        self.columns = columns
        self.grading_system = grading_system
        self.period = period
        self.elements = []
        self.student = self.computed_report.student
        self.level_group = self.student.class_room.level.level_group

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

    def create_elements(self):
        self.elements = []
        entity_table = create_header()
        student_table = create_student_table(self.computed_report)
        title = style_paragraph(self.title.upper(), heading_style2)
        body_table = create_activity_body_table(self.computed_report, self.columns)

        result_table = create_result_table(self.computed_report)
        comment_table = create_comment_table(self.computed_report)
        next_term_table = create_next_term_table()
        score_key_table = create_score_key_table()

        for element in [
                entity_table, student_table, space, title, space, body_table, space, result_table, space, comment_table, space, next_term_table, space, score_key_table
        ]:
            self.elements.append(element)
       

    @property
    def title(self):
        level_group_name = self.student.class_room.level.level_group.name
        return f'{level_group_name} - LEVEL, COMPETENCE BASED CURRICULUM TERMLY REPORT CARD'