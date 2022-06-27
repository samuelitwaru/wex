from rest_framework import viewsets
from results.serializers.report import ComputedReportSerializer

from results.utils import compute_student_report
from ..models import GradingSystem, Period, Report, Student
from ..serializers import ReportSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from ..filters import ReportFilter
from django_filters import rest_framework as filters



class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ReportFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        f = ReportFilter(self.request.GET, queryset=queryset)
        return f.queryset

    @action(detail=False, methods=['GET'], name='get_count', url_path='count')
    def get_count(self, request, *args, **kwargs):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        count = queryset.count()
        return Response({'count':count})
    
    @action(detail=False, methods=['GET'], name='get_computed_student_report', url_path=r'computed/(?P<student_id>[\w-]+)') 
    def get_student_computed_report(self, request, *args, **kwargs):
        params = self.request.query_params
        grading_system = GradingSystem.objects.filter(id=params.get('grading_system')).first()
        period = Period.objects.filter(id=params.get('period')).first()
        if not grading_system:
            grading_system = GradingSystem.objects.first()
        if not period:
            period = Period.objects.latest()
        student = Student.objects.filter(id=kwargs.get('student_id')).first()
        report_type = params.get('report_type', 'assessment')
        report = compute_student_report(student, grading_system, period, report_type=report_type)
        serializer = ComputedReportSerializer(report)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'], name='get_report_result', url_path='result') 
    def get_report_result(self, request, pk, *args, **kwargs):
        params = self.request.query_params
        grading_system = GradingSystem.objects.filter(id=params.get('grading_system')).first()
        period = Period.objects.filter(id=params.get('period')).first()
        if not grading_system:
            grading_system = GradingSystem.objects.first()
        if not period:
            period = Period.objects.latest()
        
        report = Report.objects.get(id=pk)
        student_id = report.student_id
        report = compute_student_report(student_id, grading_system, period)
        return Response({
            "points": sum([subj.points for subj in report])
        })
    
    @action(detail=False, methods=['PUT'], name='update_report_comment', url_path='comment')
    def update_report_comment(self, request, *args, **kwargs):
        data = request.data
        queryset1 = Report.objects.filter(id__in=data.get('reports'))
        queryset = queryset1
        overwrite = data.get('overwrite')
        del data['reports']
        del data['overwrite']
        if not overwrite:
            if data.get('class_teacher_comment'):
                queryset = queryset.filter(class_teacher_comment="")
            if data.get('head_teacher_comment'):
                queryset = queryset.filter(head_teacher_comment="")
        queryset.update(**data)
        serializer = self.get_serializer(queryset1, many=True)
        return Response(serializer.data)
