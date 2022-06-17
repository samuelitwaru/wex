from rest_framework import serializers
from results.serializers.paper import PaperSerializer
from results.serializers.subject import SubjectSerializer
from ..models import Level

class LevelSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    # papers = PaperSerializer(many=True, read_only=True)
    class Meta:
        model = Level
        fields = '__all__'