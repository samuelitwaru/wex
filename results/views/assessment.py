from rest_framework import viewsets

from results.serializers.assessment import MiniAssessmentSerializer
from ..serializers import AssessmentSerializer
from ..models import Assessment
from rest_framework.decorators import action
from rest_framework.response import Response


class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        teacher_pk = self.kwargs.get('teacher_pk')
        if teacher_pk:
            queryset = queryset.filter(teacher=teacher_pk)
        params = self.request.query_params
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset
    
    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return MiniAssessmentSerializer
    #     return super().get_serializer_class()

    @action(detail=False, methods=['GET'], name='get_count', url_path='count')
    def get_count(self, request, *args, **kwargs):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        count = queryset.count()
        return Response({'count':count})
    
    @action(detail=False, methods=['GET'], name='get_latest', url_path='latest')
    def get_latest(self, request, *args, **kwargs):
        queryset = super().get_queryset().last()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)