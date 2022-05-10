from random import choices
from secrets import choice
from django.db import models
from core.models import Item
from core.models import TimeStampedModel
from core.models import Department
from django.contrib.auth.models import User


ACTION_CHOICES = [
    ('CREATED', 'CREATED'),
    ('SUBMITTED', 'SUBMITTED'),
    ('APPROVED', 'APRROVED'),
    ('REJECTED', 'REJECTED'),
    ('LPO CREATED', 'LPO CREATED'),
    ('RFQ CREATED', 'RFQ CREATED'),
    ('COMPLETED', 'COMPLETED'),
]

REQUISITION_TYPE_CHOICES = [
    ('WORKS', 'WORKS'),
    ('SUPPLIES', 'SUPPLIES'),
    ('SERVICES', 'SERVICES'),
]

STATUS_CHOICES = [
    ('EDITING', 'EDITING'),
    ('SUBMITTED', 'SUBMITTED'),
    ('APPROVED', 'APPROVED'),
    ('REJECTED', 'REJECTED'),
]


class Vendor(TimeStampedModel):
    name = models.CharField(max_length=128)
    company = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    telephone = models.CharField(max_length=16)


# Create your models here.
class Requisition(TimeStampedModel):
    ref = models.CharField(max_length=128)
    subject = models.CharField(max_length=256)
    financial_year = models.CharField(max_length=16)
    requisition_type = models.CharField(max_length=16, choices=REQUISITION_TYPE_CHOICES) # works, service, supplies
    status = models.CharField(max_length=64, choices=STATUS_CHOICES) # editing, submitted, approved, rejected, completed
    comment = models.CharField(max_length=1024, null=True)

    delivery_date_min = models.DateField(null=True)
    delivery_date_max = models.DateField(null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

    # quotation = models.OneToOneField('Quotation', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # user_in_charge = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.ref


class RequisitionItem(TimeStampedModel):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=128)
    quantity = models.IntegerField()
    rate = models.IntegerField()
    metric = models.CharField(max_length=128)
    short_spec = models.CharField(max_length=512, null=True)
    long_spec = models.CharField(max_length=1024, null=True)
    requisition = models.ForeignKey('Requisition', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RequisitionAction(TimeStampedModel):
    action = models.CharField(max_length=64, choices=ACTION_CHOICES) # created, submitted, approved, rejected, LPO created, RFQ created, completed 
    comment = models.CharField(max_length=1024, null=True)
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


# class LocalPurchaseOrder(TimeStampedModel):
#     # TODO: reasearch on the fields
#     # is a doc issued by the buyer to the vendor to indicating the agreed quantities and prices for products or services that the vendor will provide to the buyer with the national or local boundaries
#     requisition = models.ForeignKey('Requisition', on_delete=models.CASCADE)
    
    

class RequestForQuotation(TimeStampedModel):
    # TODO: research on the fields
    # is a document issued by the buyer to vendor(s) to allow them submit their price quotes for the listed items in the requisition
    requisition = models.ForeignKey('Requisition', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)


class Quotation(models.Model):
    requisition_item = models.ForeignKey(RequisitionItem, on_delete=models.CASCADE)
    rate = models.IntegerField()
    metric = models.CharField(max_length=128)
    request_for_quotation = models.ForeignKey(RequestForQuotation, on_delete=models.CASCADE)


# Procurement Process
#   Initiation
#       Filling of requisition
#       Approval/Rejection of requisition
#       
#   Bidding
#       Preparation of bidding documents
#       Issuing of bidding documents
#       Submission of bidding documents
#       Opening of bidding documents
#       Selection of BEB
# 