from rest_framework import serializers
from results.serializers.paper import PaperSerializer
from results.serializers.subject import MiniSubjectSerializer, SubjectSerializer
from results.serializers.teacher import MiniTeacherSerializer
from ..models import Level


class MiniLevelSerializer(serializers.ModelSerializer):
    level_group_name = serializers.CharField(source='level_group.name', read_only=True)
    class Meta:
        model = Level
        fields = '__all__'

class LevelSerializer(MiniLevelSerializer):
    subjects = MiniSubjectSerializer(many=True, read_only=True)
    