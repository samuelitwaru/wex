from rest_framework import viewsets
from ..models import Teacher
from ..serializers import TeacherSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from core.tasks import send_welcome_mail
from rest_framework.authtoken.models import Token


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())

        return queryset

    @action(detail=True, methods=['POST'], name='upload_picture', url_path='picture/upload')
    def upload_picture(self, request, *args, **kwargs):
        picture = request.FILES['picture']
        teacher = super().get_queryset().filter(id=kwargs.get('pk')).first()
        teacher.picture = picture
        teacher.save()
        serializer = self.get_serializer(teacher)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'], name='get_count', url_path='count')
    def get_count(self, request, *args, **kwargs):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        count = queryset.count()
        return Response({'count':count})

    
    @action(detail=True, methods=['POST'], name='set_user', url_path='user')
    def set_user(self, request, *args, **kwargs):
        teacher = super().get_queryset().filter(id=kwargs.get('pk')).first()
        user = teacher.user
        data = request.data
        if user:
            user.username = data.get('username')
            user.email = data.get('email') 
            user.save()
        else:
            user = User.objects.create(**data)
            teacher.user = user
            teacher.save()
        token, created = Token.objects.get_or_create(user=user)
        serializer = self.get_serializer(teacher)
        host = request.get_host()
        send_welcome_mail.delay(host, user.username, token.key)
        return Response(serializer.data)
