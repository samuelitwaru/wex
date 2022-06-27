from rest_framework import serializers
from results.serializers.activity import ActivitySerializer

from results.serializers.level import LevelSerializer, MiniLevelSerializer
from results.serializers.teacher import MiniTeacherSerializer

from ..models import ClassRoom
from ..serializers import TeacherSerializer



class MiniClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = "__all__"


class ClassRoomSerializer(MiniClassRoomSerializer):
    teacher_detail = MiniTeacherSerializer(source='teacher', read_only=True)
    level_detail = MiniLevelSerializer(source='level', read_only=True)