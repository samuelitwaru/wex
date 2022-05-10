from procurement.models import RequisitionItem
from rest_framework import viewsets
from rest_framework import permissions
from procurement.serializers import RequisitionItemSerializer


class RequisitionItemViewSet(viewsets.ModelViewSet):
    queryset = RequisitionItem.objects.all().order_by('-created_at')
    serializer_class = RequisitionItemSerializer
