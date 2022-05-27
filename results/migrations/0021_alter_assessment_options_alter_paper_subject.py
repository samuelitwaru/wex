# Generated by Django 4.0.3 on 2022-05-27 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0020_alter_assessment_paper'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assessment',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='paper',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='results.subject'),
        ),
    ]
