# Generated by Django 4.0.3 on 2022-06-11 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0029_rename_studentreport_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='LevelGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(choices=[('P', 'Primary'), ('O', 'Ordinary'), ('A', 'Advanced')], max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='level',
            name='description',
        ),
        migrations.AlterUniqueTogether(
            name='report',
            unique_together={('student', 'period')},
        ),
    ]
