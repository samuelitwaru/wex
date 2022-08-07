import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from utils import OverwiteStorageSystem
from django_resized import ResizedImageField
from django.contrib.auth.models import User

SINGLE_ENTRY_VALIDATOR = [MinValueValidator(1), MaxValueValidator(1)]

def entity_logo_upload_loacation(instance, filename):
	_, extension = filename.split('.')
	return f'entities/pictures/{instance.id}.{extension}'

def user_signature_upload_location(instance, filename):
    _, extension = filename.split('.')
    return f'users/signatures/{instance.id}.{extension}'


# Create your models here.
class Entity(models.Model):
	id = models.IntegerField(primary_key=True, default=1, validators=SINGLE_ENTRY_VALIDATOR)
	name = models.CharField(max_length=128)
	location = models.CharField(max_length=256)
	telephone = models.CharField(max_length=16, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	logo = ResizedImageField(upload_to=entity_logo_upload_loacation, storage=OverwiteStorageSystem, null=True, blank=True)

	def __str__(self):
		return self.name


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	class Meta:
		abstract = True


class Item(TimeStampedModel):
	name = models.CharField(max_length=128)
	brand = models.CharField(max_length=128)
	description = models.CharField(max_length=1024, null=True)

	def __str__(self):
		return self.name


class MetricSystem(TimeStampedModel):
	name = models.CharField(max_length=128)
	is_standard = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	def base_metric(self):
		return self.metric_set.filter(multiplier=1.0).first()

	def convert(self, quantity, from_metric, to_metric):
		return quantity*(to_metric.multiplier/from_metric.multiplier)


class Metric(TimeStampedModel):
	unit = models.CharField(max_length=128)
	symbol = models.CharField(max_length=64)
	multiplier = models.FloatField()
	metric_system = models.ForeignKey(MetricSystem, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.unit} {self.symbol}"



class Department(TimeStampedModel):
	name = models.CharField(max_length=128, unique=True)

	def __str__(self):
		return self.name



class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='profile')
    telephone = models.CharField(max_length=16, null=True, unique=True)
    signature = ResizedImageField(upload_to=user_signature_upload_location, storage=OverwiteStorageSystem, null=True, blank=True)



    def __str__(self):
        return self.user


from django.db.models.signals import post_save


def create_user_profile(sender, instance, created, **kwargs):
	profile, created = Profile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User) 