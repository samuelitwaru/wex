from rest_framework import serializers

from results.serializers.level import LevelSerializer, MiniLevelSerializer
from results.serializers.subject import MiniSubjectSerializer, SubjectSerializer
from results.serializers.grading_system import GradingSystemSerializer
from ..models import LevelGroup


class LevelGroupSerializer(serializers.ModelSerializer):
    levels = MiniLevelSerializer(source='level_set', many=True, read_only=False)
    subjects = MiniSubjectSerializer(source='subject_set', many=True, read_only=False)
    grading_systems = GradingSystemSerializer(many=True, read_only=False)
    class Meta:
        model = LevelGroup
        fields = '__all__'
