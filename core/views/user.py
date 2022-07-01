from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from core.tasks import send_welcome_mail

from results.models import Teacher
from utils import get_host_name
from ..serializers import UserSerializer, GroupSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.exclude(is_superuser=True).all()
    serializer_class = UserSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset

    def create(self, request, *args, **kwargs):
        group_ids = request.data.pop('groups', [])
        user = User.objects.create(**request.data)
        groups = Group.objects.filter(id__in=group_ids)
        user.groups.set(groups)
        user.set_password(request.data.get('username'))
        user.save()
        if groups.filter(name='teacher').first():
            # create teacher profile
            Teacher.objects.create(
                **{
                    'name':f'{user.first_name} {user.last_name}', 
                    'initials':f'{user.first_name[0]}.{user.last_name[0]}',
                    'user':user
                }
            )

        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        user = get_object_or_404(self.queryset, pk=kwargs['pk'])
        group_ids = request.data.pop('groups', [])
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.username = request.data.get('username')
        user.email = request.data.get('email')
        user.save()
        groups = Group.objects.filter(id__in=group_ids)
        user.groups.set(groups)
        if groups.filter(name='teacher').first():
            teacher = Teacher.objects.get_or_create(
                user=user, 
                defaults={
                    'name':f'{user.first_name} {user.last_name}', 
                    'initials':f'{user.first_name[0]}.{user.last_name[0]}',
                    }
                )
            print(teacher)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


    @action(detail=False, methods=['GET'], name='get_count', url_path='count')
    def get_count(self, request, *args, **kwargs):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        count = queryset.count()
        return Response({'count':count})
    

    @action(detail=False, methods=['GET'], name='get_user_by_token', url_path=r'token/(?P<token>[\w-]+)')
    def get_user_by_token(self, request, *args, **kwargs):
        token = Token.objects.filter(key=kwargs.get('token')).first()
        if token:
            user = token.user
            res = {
                'user_id': user.pk,
                'name': f'{user.first_name} {user.last_name}',
                'email': user.email,
                'groups': [group.name for group in user.groups.all()]
            }
            if 'teacher' in res['groups']:
                teacher = Teacher.objects.filter(user=user).first()
                res['teacher_id'] = teacher.id
            return Response(res)
        return Response({})

    
    @action(detail=True, methods=['PUT'], name='update_password', url_path=r'update-password', permission_classes=[])
    def update_password(self, request, *args, **kwargs):
        user = get_object_or_404(User.objects, pk=self.kwargs['pk'])
        data = request.data
        current_password = data.get('current_password')
        
        user = authenticate(username=user.username, password=current_password)
        if user:
            print(user)
            if data['new_password'] == data['confirm_password']:
                user.set_password(data.get('new_password'))
                user.save()
                serializer = self.get_serializer(user)
                return Response(serializer.data)
            return HttpResponseBadRequest('New passwords entered do not match.')
        return HttpResponseBadRequest('Invalid current password.')
    

    @action(detail=False, methods=['POST'], name='reset_password', url_path=r'reset-password', permission_classes=[])
    def reset_password(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.filter(username=data.get('username')).first()
        if user:
            token, created = Token.objects.get_or_create(user=user)
            host = get_host_name(request)
            send_welcome_mail.delay(host, user.username, token.key)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        return HttpResponseBadRequest()
    
    @action(detail=False, methods=['GET'], name='get_count', url_path='count')
    def get_count(self, request, *args, **kwargs):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        count = queryset.count()
        return Response({'count':count})
    
    @action(detail=True, methods=['PUT'], name='activate_or_deactivate', url_path='activate')
    def activate_or_deactivate(self, request, *args, **kwargs):
        queryset = User.objects.filter(id=kwargs.get('pk'))
        queryset.update(**request.data)
        user = queryset.first()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['PUT'], name='add_groups', url_path='groups/add')
    def add_groups(self, request, *args, **kwargs):
        user = User.objects.filter(id=kwargs.get('pk')).first()
        groups = Group.objects.filter(pk__in=request.data)
        user.groups.add(*groups)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['PUT'], name='remove_groups', url_path='groups/remove')
    def remove_groups(self, request, *args, **kwargs):
        user = User.objects.filter(id=kwargs.get('pk')).first()
        groups = Group.objects.filter(pk__in=request.data)
        user.groups.remove(*groups)
        serializer = self.get_serializer(user)
        return Response(serializer.data)



class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset