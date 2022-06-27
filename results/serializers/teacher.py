from rest_framework import serializers

from core.serializers.user import UserSerializer
from ..models import Teacher, TeacherClassRoomPaper


class TeacherClassRoomPaperSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherClassRoomPaper
        fields = '__all__'




class MiniTeacherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Teacher
        fields = '__all__'

class TeacherSerializer(MiniTeacherSerializer):
    user = UserSerializer(read_only=True)