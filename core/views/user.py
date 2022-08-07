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
from permissions import HasGroup
from functools import partial


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.exclude(is_superuser=True).all()
    serializer_class = UserSerializer
    # permission_classes = [partial(HasGroup, 'dos')]

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset
    
    @action(detail=False, methods=['GET'], name='get_count', url_path='count')
    def get_count(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()
        return Response({'count':count})

    def create(self, request, *args, **kwargs):
        group_ids = request.data.pop('groups', [])
        telephone = request.data.pop('telephone', None)
        user = User.objects.create(**request.data)
        groups = Group.objects.filter(id__in=group_ids)
        user.groups.set(groups)
        user.set_password(request.data.get('username'))
        user.save()
        profile = user.profile
        profile.telephone = telephone
        profile.save()
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
        telephone = request.data.pop('telephone', None)
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.username = request.data.get('username')
        user.email = request.data.get('email')
        user.is_active = request.data.get('is_active')
        user.save()
        profile = user.profile
        profile.telephone = telephone
        profile.save()
        groups = Group.objects.filter(id__in=group_ids)
        user.groups.set(groups)
        if groups.filter(name='teacher').first():
            teacher, created = Teacher.objects.get_or_create(user=user)
            teacher.name = f'{user.first_name} {user.last_name}'
            teacher.initials = f'{user.first_name[0]}.{user.last_name[0]}'
            teacher.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

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
    
    @action(detail=True, methods=['POST'], name='upload_signature', url_path='signature/upload')
    def upload_signature(self, request, *args, **kwargs):
        picture = request.FILES['picture']
        user = super().get_queryset().filter(id=kwargs.get('pk')).first()
        profile = user.profile
        profile.signature = picture
        profile.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    # @action(detail=True, methods=['PUT'], name='add_groups', url_path='groups/add')
    # def add_groups(self, request, *args, **kwargs):
    #     user = User.objects.filter(id=kwargs.get('pk')).first()
    #     groups = Group.objects.filter(pk__in=request.data)
    #     user.groups.add(*groups)
    #     serializer = self.get_serializer(user)
    #     return Response(serializer.data)
    
    # @action(detail=True, methods=['PUT'], name='remove_groups', url_path='groups/remove')
    # def remove_groups(self, request, *args, **kwargs):
    #     user = User.objects.filter(id=kwargs.get('pk')).first()
    #     groups = Group.objects.filter(pk__in=request.data)
    #     user.groups.remove(*groups)
    #     serializer = self.get_serializer(user)
    #     return Response(serializer.data)



class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        params = self.request.query_params
        queryset = super().get_queryset()
        if params:
            queryset = queryset.filter(**params.dict())
        return queryset