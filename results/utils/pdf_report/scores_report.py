from reportlab.platypus import Paragraph, SimpleDocTemplate, Table
from .utils import *
from .competency_report import create_header

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
        for el in [header_table, self.title, space, scores_table]:
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