from rest_framework import viewsets
from ..models import Subject
from ..serializers import SubjectSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

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
    
