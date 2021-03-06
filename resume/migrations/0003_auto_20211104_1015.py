# Generated by Django 3.2.8 on 2021-11-04 07:15

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0002_alter_workexperience_end_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='address2',
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=django_resized.forms.ResizedImageField(crop=None, default='profile-pics/default.jpg', force_format=None, keep_meta=True, quality=100, size=[250, 250], upload_to='profile-pics'),
        ),
    ]
