from rest_framework import viewsets
from ..models import Activity
from ..serializers import ActivitySerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
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
    
    @action(detail=True, methods=['PUT'], name='close', url_path='close')
    def close(self, request, *args, **kwargs):
        activity = super().get_queryset().filter(id=kwargs.get('pk')).first()
        activity.is_open = False
        activity.save()
        serializer = self.get_serializer(activity)
        return Response(serializer.data)
    
    @action(detail=True, methods=['PUT'], name='open_activity', url_path='open')
    def open_activity(self, request, *args, **kwargs):
        activity = super().get_queryset().filter(id=kwargs.get('pk')).first()
        activity.is_open = True 
        activity.save()
        serializer = self.get_serializer(activity)
        return Response(serializer.data)
    