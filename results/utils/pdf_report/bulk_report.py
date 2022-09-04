from reportlab.platypus import SimpleDocTemplate, PageBreak
from .competency_report import CompetencePDFReport
from .termly_report import TermlyPDFReport
from .utils import *

class BulkPDFReport:

    def __init__(self, computed_reports, report_type, columns, grading_system, period):
        self.computed_reports = computed_reports
        self.report_type = report_type
        self.columns = columns
        self.grading_system = grading_system
        self.period = period
        self.elements = []

    def create_elements(self):
        self.elements = []
        for computed_report in self.computed_reports:
            if self.report_type == 'assessment':
                report = TermlyPDFReport(computed_report, self.columns, self.grading_system, self.period)
            else:
                report = CompetencePDFReport(computed_report, self.columns, self.grading_system, self.period)
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