from rest_framework import serializers

from results.serializers.level import LevelSerializer
from results.serializers.subject import SubjectSerializer
from ..models import LevelGroup


class LevelGroupSerializer(serializers.ModelSerializer):
    levels = LevelSerializer(source='level_set', many=True, read_only=False)
    subjects = SubjectSerializer(source='subject_set', many=True, read_only=False)
    class Meta:
        model = LevelGroup
        fields = '__all__'
