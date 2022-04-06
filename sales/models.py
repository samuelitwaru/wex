from django.db import models
from core.models import TimeStampedModel


# Create your models here.
class Product(TimeStampedModel):
    name = models.CharField(max_length=128)
    brand = models.CharField(max_length=128)
    description = models.CharField(max_length=1024, null=True)
    barcode = models.CharField(max_length=128, null=True, unique=True)
    quantity = models.FloatField(default=0)
    limit = models.FloatField(default=0)

    inventory_stock_ref = models.ForeignKey('Stock', null=True, on_delete=models.SET_NULL)

    metric_system = models.ForeignKey('MetricSystem', null=True, on_delete=models.SET_NULL)
    categories = models.ManyToManyField('ProductCategory', through='ProductCategories', through_fields=('product', 'category'))

    def __str__(self):
        return self.name


class SaleGuide(TimeStampedModel):
	metric = models.ForeignKey('Metric', on_delete=models.CASCADE)
	price = models.IntegerField()
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sale_guides')

	def __str__(self):
		return f"{self.price} @ {self.metric}"


class Sale(TimeStampedModel):
    quantity = models.IntegerField()
    metric = models.CharField(max_length=128)
    product_name = models.CharField(max_length=128)
    customer = models.CharField(max_length=128, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)


class Order(TimeStampedModel):
    order_ref = models.CharField(max_length=128)

    def __str__(self):
        return self.ref


class ProductCategory(TimeStampedModel):
    name = models.CharField(max_length=128)


class ProductCategories(TimeStampedModel):
	stock = models.ForeignKey(Product, on_delete=models.CASCADE)
	category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)