from django.urls import path
from wex import router
from .views import *

app_name = "core"

router.register(r'entities', EntityViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'items', ItemViewSet)
router.register(r'metric-systems', MetricSystemViewSet)
router.register(r'metrics', MetricViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('user/set/<str:token_key>', set_user, name='set_user'),
]