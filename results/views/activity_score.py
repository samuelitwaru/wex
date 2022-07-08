from rest_framework import viewsets

from results.utils.report_pdf import ScoresPDF
from utils import get_host_name
from ..models import ActivityScore
from ..serializers import ActivityScoreSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import os

class ActivityScoreViewSet(viewsets.ModelViewSet):
    queryset = ActivityScore.objects.all()
    serializer_class = ActivityScoreSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        activity_pk = self.kwargs.get('activity_pk')
        print(self.kwargs)
        if activity_pk:
            queryset = queryset.filter(activity=activity_pk)
        params = self.request.query_params
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset

    @action(detail=False, methods=['GET'], name='get_count', url_path='count')
    def get_count(self, request, *args, **kwargs):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        count = queryset.count()
        return Response({'count':count})
    
    @action(detail=False, methods=['GET'], name='download', url_path=r'download') 
    def download(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        pdf = ScoresPDF(queryset)
        doc = pdf.run()
        host = get_host_name(request)
        filename = os.path.basename(doc.filename)
        file_url = f'{host}/media/{filename}'
        return Response({'file_url': file_url})