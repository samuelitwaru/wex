from rest_framework import serializers
from results.serializers.period import PeriodSerializer

# from results.serializers.subject import SubjectSerializer
from ..models import Activity
# from ..serializers import MiniClassRoomSerializer


class ActivitySerializer(serializers.ModelSerializer):
    # class_room_detail = MiniClassRoomSerializer(source='class_room', read_only=True)
    # subject_detail = SubjectSerializer(source='subject', read_only=True)
    # period_detail = PeriodSerializer(source='period', read_only=True)
    class Meta:
        model = Activity
        fields = '__all__'