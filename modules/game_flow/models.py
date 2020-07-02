from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from class_room.models import User
from game_skeleton.models import HeroClass, Gift


class UserGiftManager(models.Manager):
    def get_queryset(self):
        bought_gifts = super().get_queryset().annotate(
            name=models.F('gift_class__name'),
            price=models.F('gift_class__price'),
            image=models.F('gift_class__image'),
        )
        return bought_gifts


class UserGift(models.Model):
    gift_class = models.ForeignKey(
        Gift, on_delete=models.CASCADE, related_name='user_gifts'
    )
    quantity = models.PositiveIntegerField(default=1)
    datetime_created = models.DateTimeField(auto_now=True)
    datetime_edited = models.DateTimeField(auto_now_add=True)
    hero = models.ForeignKey(
        'UserHero', on_delete=models.CASCADE, related_name='gifts'
    )

    objects = UserGiftManager()

    def __str__(self):
        return self.gift_class.name


class UserHero(models.Model):
    hero_class = models.ForeignKey(
        HeroClass, on_delete=models.CASCADE, related_name='user_heroes'
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='hero'
    )
    datetime_created = models.DateTimeField(auto_now=True)
    datetime_edited = models.DateTimeField(auto_now_add=True)

    capacity = models.FloatField(default=0)
    coins = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)

    def __str__(self):
        return self.hero_class.name


class EventHistory(models.Model):
    author = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True,
        related_name='actions'
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='events'
    )

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
