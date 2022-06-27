from rest_framework import viewsets

from results.serializers import assessment

from ..models import Score
from ..serializers import ScoreSerializer


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        assessment_pk = self.kwargs.get('assessment_pk')
        if assessment_pk:
            queryset = queryset.filter(assessment=assessment_pk)
        params = self.request.query_params
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset