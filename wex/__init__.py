from rest_framework import routers
from .celery import app as celery_app


__all__ = ('celery_app',)
router = routers.DefaultRouter()
