from rest_framework import viewsets
from ..models import TeacherClassRoomSubject
from ..serializers import TeacherClassRoomSubjectSerializer

class TeacherClassRoomSubjectViewSet(viewsets.ModelViewSet):
    queryset = TeacherClassRoomSubject.objects.all()
    serializer_class = TeacherClassRoomSubjectSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = self.queryset
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset