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

    telephone = serializers.CharField(source='profile.telephone', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password', 'groups', 'date_joined', 'teacher')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)



from rest_framework import serializers
from django.contrib.auth.models import User, Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        # fields = '__all__'
        exclude = ('permissions',)


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    telephone = serializers.CharField(source='profile.telephone', read_only=True)
    class Meta:
        model = User
        exclude = ('password',)