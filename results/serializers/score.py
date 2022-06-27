from rest_framework import serializers

from results.serializers.student import MiniStudentSerializer
from ..models import Score


class MiniScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'
        
class ScoreSerializer(MiniScoreSerializer):
    student_detail = MiniStudentSerializer(source='student', read_only=True)
    