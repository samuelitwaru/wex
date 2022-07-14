from django.apps import AppConfig, apps
from django.db.models.signals import post_migrate
app_name = 'results'

def add_groups(sender, **kwargs):
    from django.contrib.auth.models import Group
    groups = ['dos', 'teacher', 'head_teacher']
    for group in groups:
        Group.objects.get_or_create(name=group)

class ResultsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = app_name

    def ready(self):
        post_migrate.connect(add_groups, self)
        return super().ready()