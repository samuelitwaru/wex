from rest_framework import viewsets

from results.serializers import period
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
    
    @action(detail=False, methods=['PUT'], name='open_promotions', url_path='latest/open-promotions')
    def open_promotions(self, request, *args, **kwargs):
        period = super().get_queryset().last()
        if period.is_promotional:
            period.promotions_opened = True    
            period.save()
        serializer = self.get_serializer(period)
        return Response(serializer.data)
    
    @action(detail=False, methods=['PUT'], name='close_promotions', url_path='latest/close-promotions')
    def close_promotions(self, request, *args, **kwargs):
        period = super().get_queryset().last()
        if period.is_promotional:
            period.promotions_opened = False   
            period.save()
        serializer = self.get_serializer(period)
        return Response(serializer.data)
    