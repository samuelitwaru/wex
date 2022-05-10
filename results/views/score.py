from rest_framework import viewsets

from ..models import Score
from ..serializers import ScoreSerializer


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = self.queryset
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset