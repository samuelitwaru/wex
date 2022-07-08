from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from results.serializers import teacher
from results.serializers.class_room import MiniClassRoomSerializer
from ..serializers import ClassRoomSerializer
from ..models import ClassRoom, Subject, PaperAllocation
from rest_framework.response import Response
from rest_framework.decorators import action, api_view


class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        teacher_pk = self.kwargs.get('teacher_pk')
        level_pk = self.kwargs.get('level_pk')
        if teacher_pk:
            queryset = queryset.filter(teacher=teacher_pk)
        if level_pk:
            queryset = queryset.filter(teacher=level_pk)
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


@api_view(['GET'])
def get_teacher_allocated_class_rooms(request, teacher_pk):
    class_room_ids = [class_room_paper.class_room_id for class_room_paper in PaperAllocation.objects.filter(teacher=teacher_pk)]
    queryset = ClassRoom.objects.filter(id__in=class_room_ids)
    params = request.GET
    if params:
        queryset = queryset.filter(**params.dict())
    serializer = ClassRoomSerializer(queryset.all(), many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_teacher_allocated_class_room(request, teacher_pk, class_room_pk):
    class_room_ids = [class_room_paper.class_room_id for class_room_paper in PaperAllocation.objects.filter(teacher=teacher_pk)]
    queryset = ClassRoom.objects.filter(id__in=class_room_ids)
    params = request.GET
    if params:
        queryset = queryset.filter(**params.dict())
    class_room = get_object_or_404(queryset, pk=class_room_pk)
    serializer = ClassRoomSerializer(class_room)
    return Response(serializer.data)
