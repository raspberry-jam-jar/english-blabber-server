# Generated by Django 3.0.5 on 2020-04-18 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('class_room', '0002_socialuser'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='socialuser',
            unique_together={('code', 'platform')},
        ),
    ]
