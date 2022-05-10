from rest_framework import viewsets
from ..serializers import AssessmentSerializer
from ..models import Assessment


class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer