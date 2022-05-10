from rest_framework import serializers

from results.serializers.score import ScoreSerializer
from results.serializers.subject import SubjectSerializer
from results.serializers.teacher import TeacherSerializer
from ..models import Assessment
from ..serializers import ClassRoomSerializer


class AssessmentSerializer(serializers.ModelSerializer):
    # class_rooms = ClassRoomSerializer(many=True, read_only=True)
    scores = ScoreSerializer(source='score_set', many=True, read_only=True)
    class_room_detail = ClassRoomSerializer(source='class_room', read_only=True)
    teacher_detail = TeacherSerializer(source='teacher', read_only=True)
    subject_detail = SubjectSerializer(source='subject', read_only=True)
    
    class Meta:
        model = Assessment
        fields = '__all__'