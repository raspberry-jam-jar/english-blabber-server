# Generated by Django 3.0 on 2020-05-04 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_skeleton', '0002_auto_20200417_0736'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gradation',
            old_name='points_amount',
            new_name='experience',
        ),
        migrations.RenameField(
            model_name='penalty',
            old_name='points_amount',
            new_name='experience',
        ),
        migrations.AddField(
            model_name='gradation',
            name='money',
            field=models.DecimalField(
                decimal_places=4, default=0.0, max_digits=10
            ),
        ),
        migrations.AlterField(
            model_name='gift',
            name='price',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='heroclass',
            name='capacity',
            field=models.FloatField(
                help_text='How many experience points should be collected '
                          'to finish the hero class.'
            ),
        ),
    ]