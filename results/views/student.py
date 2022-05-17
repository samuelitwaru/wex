from rest_framework import viewsets
from ..models import Student
from ..serializers import StudentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset

    @action(detail=True, methods=['POST'], name='upload_picture', url_path='picture/upload')
    def upload_picture(self, request, *args, **kwargs):
        picture = request.FILES['picture']
        student = super().get_queryset().filter(id=kwargs.get('pk')).first()
        student.picture = picture
        student.save()
        serializer = self.get_serializer(student)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'], name='get_count', url_path='count')
    def get_count(self, request, *args, **kwargs):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        count = queryset.count()
        return Response({'count':count})