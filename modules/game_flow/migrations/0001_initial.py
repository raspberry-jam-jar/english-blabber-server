# Generated by Django 3.0 on 2020-04-11 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('class_room', '0001_initial'),
        ('game_skeleton', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHero',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID'
                )),
                ('datetime_created', models.DateTimeField(auto_now=True)),
                ('datetime_edited', models.DateTimeField(auto_now_add=True)),
                ('datetime_finished', models.DateTimeField(
                    blank=True, null=True
                )),
                ('capacity', models.FloatField()),
                ('hero_class', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='game_skeleton.HeroClass'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='heroes', to='class_room.User'
                )),
            ],
        ),
        migrations.CreateModel(
            name='EventHistory',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID'
                )),
                ('points', models.FloatField()),
                ('object_id', models.PositiveIntegerField()),
                ('is_draft', models.BooleanField(
                    default=False,
                    help_text='Draft note does not participate in '
                              'hero capacity calculation.'
                )),
                ('datetime_created', models.DateTimeField(auto_now=True)),
                ('datetime_edited', models.DateTimeField(auto_now_add=True)),
                ('author', models.OneToOneField(
                    null=True, on_delete=django.db.models.deletion.SET_NULL,
                    related_name='actions', to='class_room.User'
                )),
                ('content_type', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='contenttypes.ContentType'
                )),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='events', to='class_room.User'
                )),
            ],
        ),
    ]
