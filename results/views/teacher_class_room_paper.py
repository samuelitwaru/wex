from rest_framework import viewsets
from ..models import TeacherClassRoomPaper
from ..serializers import TeacherClassRoomPaperSerializer

class TeacherClassRoomPaperViewSet(viewsets.ModelViewSet):
    queryset = TeacherClassRoomPaper.objects.all()
    serializer_class = TeacherClassRoomPaperSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset
