# Generated by Django 2.2.12 on 2020-08-05 10:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class_room', '0002_socialuser_datetime_last_edited'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='learning_group',
        ),
        migrations.AddField(
            model_name='learninggroup',
            name='users',
            field=models.ManyToManyField(related_name='learning_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]
