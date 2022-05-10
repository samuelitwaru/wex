from rest_framework import serializers

from results.grade import GradeSerializer
from ..models import GradingSystem


class GradingSystemSerializer(serializers.ModelSerializer):
    grades = GradeSerializer(many=True, read_only=True)
    class Meta:
        model = GradingSystem
        fields = '__all__'