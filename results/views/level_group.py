from rest_framework import viewsets
from ..models import LevelGroup, setup_levels
from ..serializers import LevelGroupSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class LevelGroupViewSet(viewsets.ModelViewSet):
    queryset = LevelGroup.objects.all()
    serializer_class = LevelGroupSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset

    @action(detail=False, methods=['GET'], name='get_count', url_path='count')
    def get_count(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()
        return Response({'count':count})

    @action(detail=False, methods=['POST'], name='setup_levels', url_path='levels/setup')
    def setup_levels(self, request, *args, **kwargs):
        data = request.data
        setup_levels(data)
        level_groups = super().get_queryset()
        serializer = self.get_serializer(level_groups, many=True)
        return Response(serializer.data)