from rest_framework import serializers
from ..models import Level
from ..serializers import PaperSerializer

class LevelSerializer(serializers.ModelSerializer):
    papers = PaperSerializer(many=True, read_only=True)
    
    class Meta:
        model = Level
        fields = '__all__'