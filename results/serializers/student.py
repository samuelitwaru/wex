from rest_framework import serializers

from results.serializers.subject import SubjectSerializer
from ..models import Student
from ..serializers import ClassRoomSerializer


class StudentSerializer(serializers.ModelSerializer):
    class_room_detail = ClassRoomSerializer(source='class_room', read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    class Meta:
        model = Student
        fields = '__all__'