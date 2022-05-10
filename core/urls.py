from wex import router
from .views import *


router.register(r'users', UserViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'items', ItemViewSet)
router.register(r'metric-systems', MetricSystemViewSet)
router.register(r'metrics', MetricViewSet)