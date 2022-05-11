from rest_framework import viewsets
from rest_framework.decorators import action
from ..models import Level, Subject
from ..serializers import LevelSerializer
from rest_framework.response import Response


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

    @action(detail=True, methods=['PUT'], name='Add Level Subjects', url_path='subjects/add')
    def add_level_subjects(self, request, *args, **kwargs):
        request.data
        level = Level.objects.filter(id=kwargs.get('pk')).first()
        subjects = Subject.objects.filter(pk__in=request.data)
        level.subjects.add(*subjects)
        serializer = self.get_serializer(level)
        return Response(serializer.data)
    
    @action(detail=True, methods=['PUT'], name='Remove Level Subjects', url_path='subjects/remove')
    def remove_level_subjects(self, request, *args, **kwargs):
        request.data
        level = Level.objects.filter(id=kwargs.get('pk')).first()
        subjects = Subject.objects.filter(pk__in=request.data)
        level.subjects.remove(*subjects)
        # queryset = Level.objects
        serializer = self.get_serializer(level)
        return Response(serializer.data)