from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, HttpResponseNotFound
from ..forms import SetUserForm
from django.shortcuts import render, redirect
from django.contrib import messages


class AuthLoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class AuthLogoutView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if request.META.get('HTTP_AUTHORIZATION'):
            _, key = request.META.get('HTTP_AUTHORIZATION').split(' ')
            token = Token.objects.filter(key=key).first()
            if token: token.delete()
        
        return Response({}, status=status.HTTP_200_OK)


def index(request):
    return render(request, 'index/index.html')
    

def set_user(request, token_key):
    token = Token.objects.filter(key=token_key).first()
    if token:
        user = token.user
        set_user_form = SetUserForm()
        if request.method == 'POST':
            set_user_form = SetUserForm(data=request.POST)
            if set_user_form.is_valid():
                data = set_user_form.cleaned_data
                user.username = data['username']
                password = data['password']
                user.set_password(password)
                user.save()
                messages.success(request, 'Account created.')
                return redirect('core:index')
        context = {
            'set_user_form': set_user_form,
            'user': user,
        }
        return render(request, 'user/user.html', context)
    return HttpResponseNotFound() 
