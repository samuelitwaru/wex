from rest_framework import serializers

from core.serializers.user import UserSerializer
from ..models import Teacher, PaperAllocation


class PaperAllocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaperAllocation
        fields = '__all__'




class MiniTeacherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Teacher
        fields = '__all__'

class TeacherSerializer(MiniTeacherSerializer):
    user = UserSerializer(read_only=True)