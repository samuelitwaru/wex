from rest_framework import serializers
from ..models import RequisitionItem


class RequisitionItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RequisitionItem
        fields = '__all__'