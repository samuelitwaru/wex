from rest_framework import viewsets
from rest_framework.decorators import action
from ..models import Level, Subject, Paper
from ..serializers import LevelSerializer
from rest_framework.response import Response


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

    @action(detail=False, methods=['GET'], name='get_count', url_path='count')
    def get_count(self, request, *args, **kwargs):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        count = queryset.count()
        return Response({'count':count})

    @action(detail=True, methods=['PUT'], name='add_papers', url_path='papers/add')
    def add_papers(self, request, *args, **kwargs):
        level = Level.objects.filter(id=kwargs.get('pk')).first()
        papers = Paper.objects.filter(pk__in=request.data)
        subject = papers.first().subject
        level.papers.add(*papers)
        level.subjects.add(subject)
        serializer = self.get_serializer(level)
        return Response(serializer.data)
    
    @action(detail=True, methods=['PUT'], name='remove_papers', url_path='papers/remove')
    def remove_papers(self, request, *args, **kwargs):
        level = Level.objects.filter(id=kwargs.get('pk')).first()
        papers = Paper.objects.filter(pk__in=request.data)
        subject = papers.first().subject
        level.papers.remove(*papers)
        if not level.papers.filter(subject=subject).first():
            level.subjects.remove(subject)
        serializer = self.get_serializer(level)
        return Response(serializer.data)
