import django_filters
from .models import Report

class ReportFilter(django_filters.FilterSet):
    # price = django_filters.NumberFilter()
    # price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    # price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    # release_year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')
    # release_year__gt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__gt')
    # release_year__lt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__lt')

    # manufacturer__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Report
        # fields = ('student', 'period', 'class_teacher_comment', 'head_teacher_comment')
        fields = '__all__'