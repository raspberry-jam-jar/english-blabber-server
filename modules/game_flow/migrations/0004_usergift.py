# Generated by Django 2.2.12 on 2020-06-02 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_skeleton', '0002_data_migration'),
        ('game_flow', '0003_auto_20200530_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('datetime_created', models.DateTimeField(auto_now=True)),
                ('datetime_edited', models.DateTimeField(auto_now_add=True)),
                ('gift_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_gifts', to='game_skeleton.Gift')),
                ('hero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gifts', to='game_flow.UserHero')),
            ],
        ),
    ]