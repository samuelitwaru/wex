# Generated by Django 4.0.3 on 2022-06-15 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0036_subject_created_from_system'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='subsidiary',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
