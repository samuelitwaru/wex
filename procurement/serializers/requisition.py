from procurement.models import Requisition
from rest_framework import serializers




class RequisitionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Requisition
        fields = '__all__'