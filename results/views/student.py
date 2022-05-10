from rest_framework import viewsets
from ..models import Student
from ..serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = self.queryset
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset