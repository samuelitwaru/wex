from rest_framework import viewsets
from ..serializers import ClassRoomSerializer
from ..models import ClassRoom


class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer