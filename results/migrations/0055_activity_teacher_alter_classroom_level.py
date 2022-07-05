# Generated by Django 4.0.3 on 2022-07-05 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0054_alter_classroom_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='results.teacher'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='classroom',
            name='level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='results.level'),
            preserve_default=False,
        ),
    ]
