from rest_framework import viewsets
from ..models import GradingSystem
from ..serializers import GradingSystemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class GradingSystemViewSet(viewsets.ModelViewSet):
    queryset = GradingSystem.objects.all()
    serializer_class = GradingSystemSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset

    @action(detail=False, methods=['GET'], name='get_count', url_path='count')
    def get_count(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()
        return Response({'count':count})