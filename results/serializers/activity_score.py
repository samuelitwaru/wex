from rest_framework import serializers
from ..models import ActivityScore


class ActivityScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityScore
        fields = '__all__'