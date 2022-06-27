from rest_framework import serializers
from results.serializers.period import PeriodSerializer

from results.serializers.score import MiniScoreSerializer, ScoreSerializer
from results.serializers.subject import PaperSerializer
from results.serializers.teacher import TeacherSerializer, MiniTeacherSerializer
from ..models import Assessment
from ..serializers import ClassRoomSerializer, MiniClassRoomSerializer


class MiniAssessmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Assessment
        fields = '__all__'

class AssessmentSerializer(MiniAssessmentSerializer):
    scores = MiniScoreSerializer(source='score_set', many=True, read_only=True)
    class_room_detail = MiniClassRoomSerializer(source='class_room', read_only=True)
    teacher_detail = MiniTeacherSerializer(source='teacher', read_only=True)
    paper_detail = PaperSerializer(source='paper', read_only=True)
    period_detail = PeriodSerializer(source='period', read_only=True)
