from rest_framework import viewsets
from results.filters import SubjectFilter
from results.serializers.subject import MiniSubjectSerializer

from results.utils import SUBJECTS
from ..models import Subject, PaperAllocation
from ..serializers import SubjectSerializer
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django_filters import rest_framework as filters


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        level_pk = self.kwargs.get('level_pk')
        if level_pk:
            queryset = queryset.filter(level_group=level_pk)
        params = self.request.query_params
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

    @action(detail=False, methods=['GET'], name='get_system_subjects', url_path='system')
    def get_system_subjects(self, request, *args, **kwargs):
        return Response(SUBJECTS)


    @action(detail=False, methods=['GET'], name='get_added_system_subjects', url_path='system/added')
    def get_added_system_subjects(self, request, *args, **kwargs):
        added_subject_codes = [subject.code for subject in Subject.objects.all()]
        subjects = list (
                filter(
                    lambda subj: subj['code'] in added_subject_codes, SUBJECTS
                    )
                )
        return Response(subjects)
        

    @action(detail=False, methods=['GET'], name='get_unadded_system_subjects', url_path='system/unadded')
    def get_unadded_system_subjects(self, request, *args, **kwargs):
        added_subject_codes = [subject.code for subject in Subject.objects.all()]
        subjects = list (
            filter(
                lambda subj: not subj['code'] in added_subject_codes, SUBJECTS
                )
            )
        return Response(subjects)



@api_view(['GET'])
def get_teacher_subjects(request, teacher_pk):
    class_room_paper_ids = [class_room_paper.paper_id for class_room_paper in PaperAllocation.objects.filter(teacher=teacher_pk)]
    queryset = Subject.objects.filter(papers__in=class_room_paper_ids)
    params = request.GET
    if params:
        queryset = queryset.filter(**params.dict())
    serializer = MiniSubjectSerializer(queryset.all(), many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_teacher_allocated_class_room_subjects(request, teacher_pk, class_room_pk):
    subject_ids = [class_room_paper.paper.subject.id for class_room_paper in PaperAllocation.objects.filter(teacher=teacher_pk, class_room=class_room_pk)]
    queryset = Subject.objects.filter(id__in=subject_ids)
    params = request.GET
    if params:
        queryset = queryset.filter(**params.dict())
    serializer = SubjectSerializer(queryset.all(), many=True)
    return Response(serializer.data)