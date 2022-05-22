from rest_framework import serializers

from results.serializers.subject import SubjectSerializer
from ..models import Level
from ..serializers import PaperSerializer

class LevelSerializer(serializers.ModelSerializer):
    # papers = PaperSerializer(many=True, read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    class Meta:
        model = Level
        fields = '__all__'