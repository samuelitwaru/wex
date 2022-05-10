from rest_framework import serializers

from ..models import ClassRoom
from ..serializers import TeacherSerializer


class ClassRoomSerializer(serializers.ModelSerializer):
    teacher_detail = TeacherSerializer(read_only=True)
    
    class Meta:
        model = ClassRoom
        fields = "__all__"