# Generated by Django 4.0.3 on 2022-06-15 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0038_rename_subsidiary_subject_is_subsidiary'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(blank=True, related_name='students', to='results.subject'),
        ),
    ]
