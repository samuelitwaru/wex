from django.apps import AppConfig, apps
from django.db.models.signals import post_migrate
from django.db.utils import OperationalError

app_name = 'results'


def add_groups(sender, **kwargs):
    from django.contrib.auth.models import Group
    groups = ['dos', 'teacher', 'head_teacher']
    for group in groups:
        try:  # catch error if Group Table has not yet been created
            Group.objects.get_or_create(name=group)
        except OperationalError:
            break


def add_assessment_categories(sender, **kwargs):
    from .models import AssessmentCategory
    cats = ['BOT', 'MOT', 'EOT']
    for cat in cats:
        try:  # catch error if AssessmentCategory Table has not yet been created
            AssessmentCategory.objects.get_or_create(name=cat)
        except OperationalError:
            break


class ResultsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = app_name

    def ready(self):
        post_migrate.connect(add_groups, self)
        post_migrate.connect(add_assessment_categories, self)
        return super().ready()