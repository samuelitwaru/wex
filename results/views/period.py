from rest_framework import viewsets
from ..models import Period
from ..serializers import PeriodSerializer


class PeriodViewSet(viewsets.ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer