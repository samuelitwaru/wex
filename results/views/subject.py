from rest_framework import viewsets

from results.utils import SUBJECTS
from ..models import Subject
from ..serializers import SubjectSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    # parser_classes = [JSONParser]

    def get_queryset(self):
        params = self.request.query_params
        print(params)
        queryset = super().get_queryset()
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
        print(added_subject_codes)
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