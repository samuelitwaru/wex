from rest_framework import serializers

from results.serializers.student import MiniStudentSerializer
from results.serializers.class_room import MiniClassRoomSerializer
from ..models import Promotion


class PromotionSerializer(serializers.ModelSerializer):
    
    student_detail = MiniStudentSerializer(source='student', read_only=True)
    current_class_room_detail = MiniClassRoomSerializer(source='current_class_room', read_only=True)
    next_class_room_detail = MiniClassRoomSerializer(source='next_class_room', read_only=True)
    
    class Meta:
        model = Promotion
        fields = '__all__'