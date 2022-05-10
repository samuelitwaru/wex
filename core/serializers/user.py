from django.contrib.auth.models import User
from rest_framework import serializers


from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.HyperlinkedModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    date_joined = serializers.DateTimeField(
        read_only=True
    )

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password', 'groups', 'date_joined')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
