# Generated by Django 4.0.3 on 2022-08-07 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_profile_signature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='telephone',
            field=models.CharField(max_length=16, null=True, unique=True),
        ),
    ]
