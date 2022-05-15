from rest_framework import serializers
from ..models import Teacher, TeacherClassRoomPaper


class TeacherClassRoomPaperSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherClassRoomPaper
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = '__all__'