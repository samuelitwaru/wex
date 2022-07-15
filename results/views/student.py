from rest_framework import viewsets

from permissions import HasGroup
from results.filters import StudentFilter
from ..models import Student, Subject
from ..serializers import StudentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from functools import partial
from rest_framework import filters


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'middle_name']
    # permission_classes = [partial(HasGroup, 'admin')]

    def get_queryset(self):
        queryset = super().get_queryset()
        class_room_pk = self.kwargs.get('class_room_pk')
        if class_room_pk:
            queryset = queryset.filter(class_room=class_room_pk)
        params = self.request.query_params
        f = StudentFilter(queryset, params)
        queryset = f.filter()
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
        queryset = self.get_queryset()
        count = queryset.count()
        return Response({'count':count})
    
    @action(detail=True, methods=['PUT'], name='add_subjects', url_path='subjects/add')
    def add_subjects(self, request, *args, **kwargs):
        student = Student.objects.filter(id=kwargs.get('pk')).first()
        subjects = Subject.objects.filter(pk__in=request.data)
        student.subjects.add(*subjects)
        serializer = self.get_serializer(student)
        return Response(serializer.data)
    
    @action(detail=True, methods=['PUT'], name='remove_subjects', url_path='subjects/remove')
    def remove_subjects(self, request, *args, **kwargs):
        student = Student.objects.filter(id=kwargs.get('pk')).first()
        subjects = Subject.objects.filter(pk__in=request.data)
        student.subjects.remove(*subjects)
        serializer = self.get_serializer(student)
        return Response(serializer.data)