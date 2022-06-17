from rest_framework import serializers
from ..models import Paper

class PaperSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.__str__', read_only=True)
    class Meta:
        model = Paper
        fields = '__all__'