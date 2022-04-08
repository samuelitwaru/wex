from django.db import models
from core.models import Item
from core.models import TimeStampedModel
from core.models import Department
from django.contrib.auth.models import User


# Create your models here.
class Requisition(TimeStampedModel):
    ref = models.CharField(max_length=128)
    subject = models.CharField(max_length=256)
    financial_year = models.CharField(max_length=16)
    requisition_type = models.CharField(max_length=16) # works, service, supplies
    status = models.CharField(max_length=64) # editing, submitted, approved, rejected, completed
    comments = models.CharField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # user_in_charge = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)


class RequisitionItem(TimeStampedModel):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=128)
    model = models.CharField(max_length=128)
    rate = models.IntegerField()
    quantity = models.IntegerField()
    metric = models.CharField(max_length=128)
    short_spec = models.CharField(max_length=512)
    long_spec = models.CharField(max_length=1024)


class RequisitionAction(TimeStampedModel):
    action = models.CharField(max_length=64) # created, submitted, approved, rejected, LPO created, RFQ created, completed 
    requisition = models.ForeignKey('Requisition', on_delete=models.CASCADE)


class LocalPurchaseOrder(TimeStampedModel):
    # TODO: reasearch on the fields
    requisition = models.ForeignKey('Requisition', on_delete=models.CASCADE)


class RequestForQuotation(TimeStampedModel):
    # TODO: research on the fields
    requisition = models.ForeignKey('Requisition', on_delete=models.CASCADE)



class Purchase(TimeStampedModel):
    quantity = models.IntegerField()
    product_name = models.CharField(max_length=128)
    purchase_price = models.IntegerField()
    purchase_metric = models.CharField(max_length=128)

    export_ref = models.CharField(max_length=64) # TODO: find out if we can have a function to generate default value for model fields
    exported = models.BooleanField(default=False)
    
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    requisition = models.ForeignKey('Requisition', on_delete=models.CASCADE)
    