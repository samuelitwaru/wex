from rest_framework import viewsets
from ..models import Paper
from ..serializers import PaperSerializer

class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer