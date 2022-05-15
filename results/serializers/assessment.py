from rest_framework import serializers
from results.serializers.period import PeriodSerializer

from results.serializers.score import ScoreSerializer
from results.serializers.subject import PaperSerializer
from results.serializers.teacher import TeacherSerializer
from ..models import Assessment
from ..serializers import ClassRoomSerializer


class AssessmentSerializer(serializers.ModelSerializer):
    # class_rooms = ClassRoomSerializer(many=True, read_only=True)
    scores = ScoreSerializer(source='score_set', many=True, read_only=True)
    class_room_detail = ClassRoomSerializer(source='class_room', read_only=True)
    teacher_detail = TeacherSerializer(source='teacher', read_only=True)
    paper_detail = PaperSerializer(source='paper', read_only=True)
    period_detail = PeriodSerializer(source='period', read_only=True)
    
    class Meta:
        model = Assessment
        fields = '__all__'