from rest_framework import serializers
from ..models import Teacher, TeacherClassRoomSubject


class TeacherClassRoomSubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherClassRoomSubject
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = '__all__'