from rest_framework import serializers
from ..models import UserPref


class UserPrefSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPref
        fields = '__all__'