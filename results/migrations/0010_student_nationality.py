# Generated by Django 4.0.3 on 2022-07-28 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0009_student_index_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='nationality',
            field=models.CharField(default='Ugandan', max_length=128),
            preserve_default=False,
        ),
    ]
