from django.contrib.auth.models import Group
from django.apps import apps
from django.conf import settings
import json
import os.path

models = [model._meta.model_name for model in apps.get_app_config('results').get_models()]
function_categories = 'CRUD'
user_groups = [group.name for group in Group.objects.all()]

def generate_functionality_files():
    for group in user_groups:
        content = dict()
        for model in models:
            content[model] = default_funcs(model)
        path = f'{settings.MEDIA_ROOT}functionalities/{group}.json'
        if not os.path.exists(path):
            with open(f'{settings.MEDIA_ROOT}functionalities/{group}.json', 'w') as file:
                content = json.dumps(content) 
                file.write(content)


def default_funcs(model):
    return {
        'C': [{'func': f'create_{model}', 'limits':[]}],
        'R': [{'func': f'read_{model}', 'limits':[]}],
        'U': [{'func': f'update_{model}', 'limits':[]}],
        'D': [{'func': f'delete_{model}', 'limits':[]}]
    }

    
