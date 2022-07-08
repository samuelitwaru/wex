from rest_framework import viewsets
from rest_framework.decorators import action
from results.serializers import assessment
from rest_framework.response import Response

from results.utils.report_pdf import ScoresPDF
from utils import get_host_name
from ..models import Score
from ..serializers import ScoreSerializer
import os


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
    
    @action(detail=False, methods=['GET'], name='download', url_path=r'download') 
    def download(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        pdf = ScoresPDF(queryset)
        doc = pdf.run()
        host = get_host_name(request)
        filename = os.path.basename(doc.filename)
        file_url = f'{host}/media/{filename}'
        return Response({'file_url': file_url})
       