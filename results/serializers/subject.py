from rest_framework import serializers

from results.serializers.paper import PaperSerializer
from ..models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    papers = PaperSerializer(source='paper_set', read_only=True, many=True)
    class Meta:
        model = Subject
        fields = '__all__'