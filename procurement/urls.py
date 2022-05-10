from wex import router
from .views import *


router.register(r'requisitions', RequisitionViewSet)
router.register(r'requisition-items', RequisitionItemViewSet)