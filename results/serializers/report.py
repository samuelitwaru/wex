from rest_framework import serializers
from results.serializers.paper import PaperSerializer

from results.serializers.student import StudentSerializer
from results.serializers.subject import SubjectSerializer
from ..models import Report


class ReportSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    class Meta:
        model = Report
        fields = '__all__'


class PaperReportSerializer(serializers.Serializer):
    paper = PaperSerializer()
    scores = serializers.ListField()
    total = serializers.IntegerField()
    average = serializers.IntegerField()
    score = serializers.DecimalField(max_digits=2, decimal_places=1)
    descriptor = serializers.CharField()

class SubjectReportSerializer(serializers.Serializer):
    subject = SubjectSerializer()
    papers = PaperReportSerializer(many=True)
    average = serializers.IntegerField()
    aggregate = serializers.IntegerField()
    letter_grade = serializers.CharField()
    points = serializers.IntegerField()
