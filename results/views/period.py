from rest_framework import viewsets
from ..models import Period
from ..serializers import PeriodSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class PeriodViewSet(viewsets.ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset

    @action(detail=False, methods=['GET'], name='get_latest', url_path='latest')
    def get_latest(self, request, *args, **kwargs):
        queryset = super().get_queryset().last()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)