from django.db.models.signals import post_save
from django.dispatch import receiver

from class_room.models import User
from game_flow.models import UserHero
from game_skeleton.models import HeroClass


@receiver(post_save, sender=User)
def attach_hero_to_student(instance, created, **kwargs):
    """
    Create and attach root class hero to the student user on creation.

    :param instance:
    :param created:
    :param kwargs:
    :return:
    """

    if created and instance.role == 'student':
        base_hero_class = \
            HeroClass.objects. \
            exclude(is_draft=True). \
            filter(parent__isnull=True). \
            first()
        UserHero.objects.create(hero_class=base_hero_class, user=instance)
