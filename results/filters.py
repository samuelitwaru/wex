import django_filters
from .models import Report

class ReportFilter(django_filters.FilterSet):
    class_teacher_commented =django_filters.CharFilter(field_name='class_teacher_comment', method='class_teacher_commented_filter')
    head_teacher_commented =django_filters.CharFilter(field_name='head_teacher_comment', method='head_teacher_commented_filter')

    class Meta:
        model = Report
        fields = ('student__class_room', 'period', 'class_teacher_comment', 'head_teacher_comment')
    
    def class_teacher_commented_filter(self, queryset, name, value):
        if value == 'yes':
            return queryset.exclude(class_teacher_comment="")
        elif value == 'no':
            return queryset.filter(class_teacher_comment="")
    
    def head_teacher_commented_filter(self, queryset, name, value):
        if value == 'yes':
            return queryset.exclude(head_teacher_comment="")
        elif value == 'no':
            return queryset.filter(head_teacher_comment="")