# Generated by Django 4.0.3 on 2022-07-06 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0055_activity_teacher_alter_classroom_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='skills',
            field=models.JSONField(default=[]),
            preserve_default=False,
        ),
    ]
