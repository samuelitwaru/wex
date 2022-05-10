from procurement.models import Requisition
from rest_framework import viewsets
from rest_framework import permissions
from procurement.serializers import RequisitionSerializer


class RequisitionViewSet(viewsets.ModelViewSet):
    queryset = Requisition.objects.all().order_by('-created_at')
    serializer_class = RequisitionSerializer
    # permission_classes = [permissions.IsAuthenticated]