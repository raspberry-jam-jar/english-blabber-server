from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from class_room.models import User
from game_skeleton.models import HeroClass


class UserHero(models.Model):
    hero_class = models.OneToOneField(HeroClass, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='heroes'
    )
    datetime_created = models.DateTimeField(auto_now=True)
    datetime_edited = models.DateTimeField(auto_now_add=True)
    datetime_finished = models.DateTimeField(null=True, blank=True)

    capacity = models.FloatField()


class EventHistory(models.Model):
    author = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True,
        related_name='actions'
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='events'
    )
    # If cost of the action will change it should not influence to the history
    points = models.FloatField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    event = GenericForeignKey()

    is_draft = models.BooleanField(
        default=False,
        help_text='Draft note does not participate in '
                  'hero capacity calculation.'
    )

    datetime_created = models.DateTimeField(auto_now=True)
    datetime_edited = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'User`s history events'
