from rest_framework import serializers
from results.serializers.period import PeriodSerializer

# from results.serializers.subject import SubjectSerializer
from ..models import Activity
# from ..serializers import MiniClassRoomSerializer


class ActivitySerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name')
    class Meta:
        model = Activity
        fields = '__all__'