from rest_framework import viewsets
from ..models import MetricSystem
from ..serializers import MetricSystemSerializer

class MetricSystemViewSet(viewsets.ModelViewSet):
    queryset = MetricSystem.objects.all()
    serializer_class = MetricSystemSerializer