from rest_framework import serializers
from results.serializers.class_room import ClassRoomSerializer
from results.serializers.subject import SubjectSerializer

from results.serializers.teacher import TeacherSerializer
from ..models import TeacherClassRoomSubject

class TeacherClassRoomSubjectSerializer(serializers.ModelSerializer):
    teacher_detail = TeacherSerializer(source='teacher', read_only=True)
    class_room_detail = ClassRoomSerializer(source='class_room', read_only=True)
    subject_detail = SubjectSerializer(source='subject', read_only=True)

    class Meta:
        model = TeacherClassRoomSubject
        fields = '__all__'