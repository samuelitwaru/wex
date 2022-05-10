from rest_framework import serializers

from results.serializers.student import StudentSerializer
from ..models import Score, Student


class ScoreSerializer(serializers.ModelSerializer):
    student_detail = StudentSerializer(read_only=True)
    class Meta:
        model = Score
        fields = '__all__'