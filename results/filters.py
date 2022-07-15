import django_filters
from .models import LevelGroup, PaperAllocation, Report, Subject
from rest_framework import filters


class BaseFilter:
    def __init__(self, queryset, params) -> None:
        self.queryset = queryset
        self.params = params.dict()
        self.exception_param_values = {}
        self.remove_exception_params()

    def remove_exception_params(self):
        for param in self.exception_param_handlers.keys():
            if self.params.get(param):
                self.exception_param_values[param] = self.params.get(param)
                del self.params[param]
    
    def handle_exception_params(self):
        for name, value in self.exception_param_values.items():
            handler = getattr(self, self.exception_param_handlers[name])
            self.queryset = handler(self.queryset, name, value)
            print(self.queryset)
         
    def filter(self):
        self.handle_exception_params()

        if self.params:
            self.queryset = self.queryset.filter(**self.params)
        return self.queryset


class ReportFilter(BaseFilter):
    exception_param_handlers = {
        'class_teacher_commented': 'class_teacher_commented_filter',
        'head_teacher_commented': 'head_teacher_commented_filter',
        'promotion_added': 'promotion_added_filter',
    }

    def class_teacher_commented_filter(self, queryset, name, value):
        if value == 'yes':
            return queryset.exclude(class_teacher_comment="")
        elif value == 'no':
            return queryset.filter(class_teacher_comment="")
        return queryset
    
    def head_teacher_commented_filter(self, queryset, name, value):
        if value == 'yes':
            return queryset.exclude(head_teacher_comment="")
        elif value == 'no':
            return queryset.filter(head_teacher_comment="")
        return queryset
    
    def promotion_added_filter(self, queryset, name, value):
        if value == 'yes':
            return queryset.exclude(promo_to_class_room=None)
        elif value == 'no':
            return queryset.filter(promo_to_class_room="")
        return queryset


class StudentFilter(BaseFilter):
    exception_param_handlers = {
        'search': 'search_string_handler',
    }

    def search_string_handler(self, queryset, name, value):
        # if value:
        #     queryset = queryset.filter(name)
        return queryset

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


class PaperAllocationFilter(django_filters.FilterSet):
    teacher = django_filters.CharFilter(field_name='teacher', method='teacher_filter')
    
    class Meta:
        model = PaperAllocation
        fields = ('paper__subject', 'paper', 'teacher', 'class_room')
    
    def teacher_filter(self, queryset, name, value):
        if value == '0':
            return queryset.filter(teacher=None)
        else:
            return queryset.filter(teacher=value)
        