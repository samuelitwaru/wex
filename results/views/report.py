import json
from django.http import FileResponse
from rest_framework import viewsets
from results.serializers.report import ComputedReportSerializer
from results.utils.pdf_report.competency_report import CompetencePDFReport
from results.utils.pdf_report.termly_report import TermlyPDFReport
from utils import get_host_name
from results.utils import compute_student_report
from results.utils.pdf_report.bulk_report import BulkPDFReport
from ..models import ClassRoom, GradingSystem, Period, Report, Student
from ..serializers import ReportSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from ..filters import ReportFilter
import os
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        class_room_pk = self.kwargs.get('class_room_pk')
        if class_room_pk:
            queryset = queryset.filter(promo_from_class_room=class_room_pk)
        params = self.request.query_params
        f = ReportFilter(queryset, params)
        queryset = f.filter()
        return queryset

    @action(detail=False, methods=['GET'], name='get_count', url_path='count')
    def get_count(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()
        return Response({'count': count})

    # @method_decorator(cache_page(60 * 15))
    @action(detail=False,
            methods=['GET'],
            name='get_computed_student_report',
            url_path=r'computed/(?P<student_id>[\w-]+)')
    def get_student_computed_report(self, request, *args, **kwargs):
        params = self.request.query_params
        period = Period.objects.filter(id=params.get('period')).first()
        if not period:
            period = Period.objects.latest()
        student = Student.objects.filter(id=kwargs.get('student_id')).first()
        level_group = student.class_room.level.level_group
        grading_system = GradingSystem.objects.filter(
            is_default=True, level_group=level_group).first()
        report, computed_report = compute_student_report(
            student, grading_system, period)
        serializer = ComputedReportSerializer(computed_report)
        report.computation = serializer.data
        report.save()
        return Response(serializer.data)

    @action(detail=False,
            methods=['POST'],
            name='download_student_report',
            url_path=r'computed/(?P<student_id>[\w-]+)/download')
    def download_student_report(self, request, *args, **kwargs):
        params = self.request.query_params
        period = Period.objects.filter(id=params.get('period')).first()
        if not period:
            period = Period.objects.latest()
        student = Student.objects.filter(id=kwargs.get('student_id')).first()
        level_group = student.class_room.level.level_group
        grading_system = GradingSystem.objects.filter(
            is_default=True, level_group=level_group).first()
        res = cache.get(f'computed_report{student.id}')
        if res:
            report, computed_report = res
        else:
            report, computed_report = cache.get_or_set(
                f'computed_report{student.id}', 
                compute_student_report(student, grading_system, period)
                )
        serializer = ComputedReportSerializer(computed_report)
        columns = request.data.get('columns')
        report_type = request.data.get('report_type')
        if report_type == 'activity':
            pdf_report = CompetencePDFReport(computed_report,
                               columns=columns,
                               grading_system=grading_system,
                               period=period
                               )
        else:
            pdf_report = TermlyPDFReport(computed_report,
                                columns=columns,
                                grading_system=grading_system,
                                period=period)
        
        doc = pdf_report.run()
        filename = os.path.basename(doc.filename)
        host = get_host_name(request)
        file_url = f'{host}/media/{filename}'
        report.computation = serializer.data
        report.save()
        return Response({'file_url': file_url})

    @action(detail=True,
            methods=['GET'],
            name='get_report_result',
            url_path='result')
    def get_report_result(self, request, pk, *args, **kwargs):
        params = self.request.query_params
        grading_system = GradingSystem.objects.filter(
            id=params.get('grading_system')).first()
        period = Period.objects.filter(id=params.get('period')).first()
        if not grading_system:
            grading_system = GradingSystem.objects.first()
        if not period:
            period = Period.objects.latest()

        report = Report.objects.get(id=pk)
        student_id = report.student_id
        report = compute_student_report(student_id, grading_system, period)
        return Response({"points": sum([subj.points for subj in report])})

    @action(detail=False,
            methods=['PUT'],
            name='update_report_comment',
            url_path='comment')
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
    
    @action(detail=False,
            methods=['PUT'],
            name='update_report_competency_comment',
            url_path='competency/comment')
    def update_report_competency_comment(self, request, *args, **kwargs):
        data = request.data
        queryset1 = Report.objects.filter(id__in=data.get('reports'))
        queryset = queryset1
        overwrite = data.get('overwrite')
        del data['reports']
        del data['overwrite']
        if not overwrite:
            if data.get('competency_class_teacher_comment'):
                queryset = queryset.filter(competency_class_teacher_comment="")
            if data.get('competency_head_teacher_comment'):
                queryset = queryset.filter(competency_head_teacher_comment="")
        queryset.update(**data)
        serializer = self.get_serializer(queryset1, many=True)
        return Response(serializer.data)

    @action(detail=False,
            methods=['POST'],
            name='download_class_room_report',
            url_path=r'computed/class-rooms/(?P<class_room_id>[\w-]+)/download'
            )
    def download_class_room_reports(self, request, *args, **kwargs):
        data = self.request.data
        params = self.request.query_params
        class_room_id = kwargs.get('class_room_id')

        period = Period.objects.filter(id=params.get('period')).first()
        if not period:
            period = Period.objects.latest()

        class_room = ClassRoom.objects.filter(id=class_room_id).first()
        grading_system = GradingSystem.objects.filter(
            is_default=True, level_group=class_room.level.level_group).first()
        students = Student.objects.filter(class_room=class_room).all()
        computed_reports = [
            compute_student_report(stud, grading_system, period)[1]
            for stud in students
        ]
        report_type = data.get('report_type', 'assessment')
        columns = data.get('columns', {'code': True})
        res = cache.get(f'class_room_report_{class_room.id}')
        if res:
            bulk_report = res
        else:
            bulk_report = BulkPDFReport(computed_reports, report_type, columns,
                                    grading_system, period)
            cache.set(f'class_room_report_{class_room.id}', bulk_report)
        doc = bulk_report.run()
        filename = os.path.basename(doc.filename)
        host = get_host_name(request)
        file_url = f'{host}/media/{filename}'
        return Response({'file_url': file_url})

    @action(detail=False,
            methods=['POST'],
            name='add_promotions',
            url_path='promotions/add')
    def add_promotions(self, request, *args, **kwargs):
        data = request.data
        report_ids = data.get('reports')
        to_class_room = data.get('promo_to_class_room')
        from_class_room = data.get('promo_from_class_room')
        report_qs = Report.objects.filter(id__in=report_ids)
        report_qs.update(promo_from_class_room=from_class_room,
                         promo_to_class_room=to_class_room)
        serializer = self.get_serializer(report_qs, many=True)
        return Response(serializer.data)

    @action(detail=False,
            methods=['PUT'],
            name='approve_promotions',
            url_path='approve')
    def approve_promotions(self, request, *args, **kwargs):
        data = request.data
        report_ids = data.get('promotions')
        report_qs = Report.objects.filter(id__in=report_ids)
        report_qs.update(promo_is_approved=True)
        serializer = self.get_serializer(report_qs, many=True)
        return Response(serializer.data)

    @action(detail=False,
            methods=['PUT'],
            name='reject_promotions',
            url_path='reject')
    def reject_promotions(self, request, *args, **kwargs):
        data = request.data
        report_ids = data.get('promotions')
        report_qs = Report.objects.filter(id__in=report_ids)
        report_qs.update(promo_is_approved=False)
        serializer = self.get_serializer(report_qs, many=True)
        return Response(serializer.data)