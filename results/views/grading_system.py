from rest_framework import viewsets
from ..models import GradingSystem
from ..serializers import GradingSystemSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class GradingSystemViewSet(viewsets.ModelViewSet):
    queryset = GradingSystem.objects.all()
    serializer_class = GradingSystemSerializer

    @action(detail=False, methods=['GET'], name='get_count', url_path='count')
    def get_count(self, request, *args, **kwargs):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        count = queryset.count()
        return Response({'count':count})