from rest_framework import serializers
from results.serializers.class_room import ClassRoomSerializer, MiniClassRoomSerializer
from results.serializers.paper import PaperSerializer

from results.serializers.teacher import MiniTeacherSerializer, TeacherSerializer
from ..models import TeacherClassRoomPaper

class TeacherClassRoomPaperSerializer(serializers.ModelSerializer):
    teacher_detail = MiniTeacherSerializer(source='teacher', read_only=True)
    class_room_detail = MiniClassRoomSerializer(source='class_room', read_only=True)
    paper_detail = PaperSerializer(source='paper', read_only=True)

    class Meta:
        model = TeacherClassRoomPaper
        fields = '__all__'