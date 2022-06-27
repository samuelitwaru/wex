from rest_framework import serializers

from results.serializers.subject import SubjectSerializer
from ..models import Student
from ..serializers import ClassRoomSerializer

class MiniStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class StudentSerializer(MiniStudentSerializer):
    class_room_detail = ClassRoomSerializer(source='class_room', read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
