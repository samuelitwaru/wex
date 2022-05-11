from rest_framework import serializers
from ..models import Level
from ..serializers import SubjectSerializer

class LevelSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    
    class Meta:
        model = Level
        fields = '__all__'