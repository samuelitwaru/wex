from rest_framework import serializers

from results.serializers.user import UserSerializer
from ..models import Teacher, TeacherClassRoomPaper


class TeacherClassRoomPaperSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherClassRoomPaper
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Teacher
        fields = '__all__'