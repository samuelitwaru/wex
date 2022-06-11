# Generated by Django 4.0.3 on 2022-06-11 04:27

from django.db import migrations, models
import django_resized.forms
import results.models
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0025_alter_teacher_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='picture',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=-1, size=[200, 200], storage=utils.OverwiteStorageSystem, upload_to=results.models.student_picture_upload_loacation),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='picture',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=-1, size=[200, 200], storage=utils.OverwiteStorageSystem, upload_to=results.models.teacher_picture_upload_loacation),
        ),
    ]
