import django_filters
from .models import LevelGroup, Report, Subject

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



class SubjectFilter(django_filters.FilterSet):
    level_group_name = django_filters.CharFilter(field_name='level_group', method='level_group_name_filter')
    
    class Meta:
        model = Subject
        fields = '__all__'
    
    def level_group_name_filter(self, queryset, name, value):
        level_group = LevelGroup.objects.filter(name=value).first()
        if level_group:
            return queryset.filter(level_group=level_group)
        return queryset
        