from rest_framework import serializers
from ..models import Student
from ..serializers import ClassRoomSerializer


class StudentSerializer(serializers.ModelSerializer):
    class_room_detail = ClassRoomSerializer(source='class_room', read_only=True)
    class Meta:
        model = Student
        fields = '__all__'