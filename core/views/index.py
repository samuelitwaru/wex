from multiprocessing import context
from django.shortcuts import render
from django.conf import settings
import os, json


def index(request):
    return render(request, 'index/index.html')


def functionalities(request, group):
    path = f'{settings.MEDIA_ROOT}functionalities/{group}.json'
    data = {}
    if os.path.exists(path):
        with open(f'{settings.MEDIA_ROOT}functionalities/{group}.json', 'r') as file:
            content = file.read()
            data = json.loads(content)
    context = {
        "data": data,
        "group": group
    }
    return render(request, 'index/functionalities.html', context)

def model_functionalities(request, group, model):
    path = f'{settings.MEDIA_ROOT}functionalities/{group}.json'
    data = {}
    if os.path.exists(path):
        with open(f'{settings.MEDIA_ROOT}functionalities/{group}.json', 'r') as file:
            content = file.read()
            data = json.loads(content)
    if model:
        data = data.get(model, {})
    
    context = {
        "data": data,
        "group": group
    }
    return render(request, 'index/model-functionalities.html', context)