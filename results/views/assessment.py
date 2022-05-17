from rest_framework import viewsets
from ..serializers import AssessmentSerializer
from ..models import Assessment
from rest_framework.decorators import action
from rest_framework.response import Response


class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

    def get_queryset(self):
        params = self.request.query_params
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
    
    @action(detail=False, methods=['GET'], name='get_latest', url_path='latest')
    def get_latest(self, request, *args, **kwargs):
        queryset = super().get_queryset().last()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)