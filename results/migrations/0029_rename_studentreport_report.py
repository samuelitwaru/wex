# Generated by Django 4.0.3 on 2022-06-11 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0028_alter_studentreport_period_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StudentReport',
            new_name='Report',
        ),
    ]
