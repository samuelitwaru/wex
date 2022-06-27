from rest_framework import serializers
from results.serializers.activity import ActivitySerializer
# from results.serializers.level_group import LevelGroupSerializer

from results.serializers.paper import PaperSerializer
from ..models import Subject




class MiniSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'



class SubjectSerializer(MiniSubjectSerializer):
    activities = ActivitySerializer(source='activity_set', read_only=True, many=True)
    papers = PaperSerializer(read_only=True, many=True)
    # level_group_name = LevelGroupSerializer(source='level_group.name')
