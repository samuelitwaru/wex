from rest_framework import serializers
from ..models import AssessmentCategory

class AssessmentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentCategory
        fields = '__all__'