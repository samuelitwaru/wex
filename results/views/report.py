from rest_framework import viewsets
from results.serializers import grading_system
from results.serializers.report import SubjectReportSerializer

from results.utils import compute_student_report
from ..models import GradingSystem, Period, Report
from ..serializers import ReportSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from ..filters import ReportFilter


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        f = ReportFilter(self.request.GET, queryset=queryset)
        print(dir(f))
        print(f.queryset)
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset

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
            
        student_id = kwargs.get('student_id')
        report = compute_student_report(student_id, grading_system, period)
        serializer = SubjectReportSerializer(report, many=True)
        return Response(serializer.data)
        