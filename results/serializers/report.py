from rest_framework import serializers
from results.serializers.class_room import MiniClassRoomSerializer
from results.serializers.level import MiniLevelSerializer
from results.serializers.paper import PaperSerializer

from results.serializers.student import MiniStudentSerializer, StudentSerializer
from results.serializers.subject import MiniSubjectSerializer, SubjectSerializer
from results.serializers.activity import ActivitySerializer
from ..models import Report


class ReportSerializer(serializers.ModelSerializer):
    level = MiniLevelSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    promo_from_class_room_detail = MiniClassRoomSerializer(source='promo_from_class_room', read_only=True)
    promo_to_class_room_detail = MiniClassRoomSerializer(source='promo_to_class_room', read_only=True)
    class Meta:
        model = Report
        # fields = '__all__'
        exclude = ('computation',)


class PaperReportSerializer(serializers.Serializer):
    paper = PaperSerializer()
    scores = serializers.ListField()
    total = serializers.IntegerField()
    average = serializers.IntegerField()
    aggregate = serializers.IntegerField()
    score = serializers.DecimalField(max_digits=2, decimal_places=1)
    descriptor = serializers.CharField()


class ActivityReportSerializer(serializers.Serializer):
    activity = ActivitySerializer()
    mark = serializers.IntegerField()
    score = serializers.DecimalField(max_digits=2, decimal_places=1)
    descriptor = serializers.CharField()


class SubjectReportSerializer(serializers.Serializer):
    subject = MiniSubjectSerializer()
    papers = PaperReportSerializer(many=True)
    activities = ActivityReportSerializer(many=True)
    average = serializers.IntegerField()
    aggregate = serializers.IntegerField()
    letter_grade = serializers.CharField()
    subject_teacher_initials = serializers.CharField()
    points = serializers.IntegerField()
    activity_total_scores = serializers.IntegerField()
    activity_average_score = serializers.IntegerField()
    activity_score = serializers.IntegerField()
    activity_score_identifier = serializers.CharField()


class ComputedReportSerializer(serializers.Serializer):
    report = ReportSerializer()
    subject_reports = SubjectReportSerializer(many=True)
    average = serializers.IntegerField()
    aggregates = serializers.IntegerField()
    points = serializers.IntegerField()