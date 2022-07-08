from rest_framework import serializers

from results.serializers.class_room import MiniClassRoomSerializer
from results.serializers.grading_system import GradingSystemSerializer
from results.serializers.subject import MiniSubjectSerializer
from ..models import CustomGradingSystem


class CustomGradingSystemSerializer(serializers.ModelSerializer):
    class_room_detail = MiniClassRoomSerializer(source='class_room', read_only=True)
    subject_detail = MiniSubjectSerializer(source='subject', read_only=True)
    grading_system_detail = GradingSystemSerializer(source='grading_system', read_only=True)
    class Meta:
        model = CustomGradingSystem
        fields = '__all__'