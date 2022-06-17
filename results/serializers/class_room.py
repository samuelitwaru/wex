from rest_framework import serializers

from results.serializers.level import LevelSerializer

from ..models import ClassRoom
from ..serializers import TeacherSerializer


class ClassRoomSerializer(serializers.ModelSerializer):
    teacher_detail = TeacherSerializer(source='teacher', read_only=True)
    level_detail = LevelSerializer(source='level', read_only=True)
    
    class Meta:
        model = ClassRoom
        fields = "__all__"