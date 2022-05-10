from rest_framework import serializers
from ..models import MetricSystem

class MetricSystemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MetricSystem
        fields = '__all__'