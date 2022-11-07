from django.db import models

from core.models import Item, TimeStampedModel

# Create your models here.


class Good(Item):
    barcode = models.CharField(max_length=128, null=True, unique=True)
    quantity = models.FloatField(default=0)
    limit = models.FloatField(default=0)
    # raw material, finished product
    item_type = models.CharField(max_length=64)

    export_ref = models.CharField(max_length=64, null=True)
    procurement_ref = models.CharField(max_length=64, null=True)

    metric_system = models.ForeignKey(
        'MetricSystem', null=True, on_delete=models.SET_NULL)
    categories = models.ManyToManyField(
        'GoodCategory', through='GoodCategories', through_fields=('good', 'category'))

    def __str__(self):
        return self.name


class Usage(TimeStampedModel):
    quantity = models.FloatField()
    metric = models.CharField(max_length=128)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(
        'Department', on_delete=models.SET_NULL, null=True)


class GoodCategory(TimeStampedModel):
    name = models.CharField(max_length=128)


class GoodCategories(TimeStampedModel):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    category = models.ForeignKey(GoodCategory, on_delete=models.CASCADE)
