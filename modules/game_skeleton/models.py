from decimal import Decimal

from django.contrib.postgres.fields import ArrayField
from django.db import models


class HeroClass(models.Model):
    name = models.CharField(max_length=500)
    parent = models.OneToOneField(
        'HeroClass', on_delete=models.SET_NULL, null=True, blank=True
    )
    capacity = models.FloatField(
        help_text='How many experience points should be collected '
                  'to finish the hero class.'
    )
    image = models.ImageField(upload_to='hero_class/', null=True, blank=True)
    is_draft = models.BooleanField(default=True)
    skill_ids = ArrayField(models.PositiveIntegerField(), default=list)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Hero classes'


class HeroSkill(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class GiftsManager(models.Manager):
    def get_available(self, user, quantity=1):
        gifts_qs = self.get_queryset() \
            .exclude(is_published=False)\
            .exclude(
            hero_class_id__gt=user.hero.hero_class_id
        )

        if not user.learning_group:
            gifts_qs = gifts_qs.exclude(is_group_wide=True)

            gifts_qs = gifts_qs.annotate(
                can_buy=models.Case(
                    models.When(
                        price__lte=user.hero.coins/quantity, then=True
                    ),
                    default=False, output_field=models.BooleanField()
                )
            )
        else:
            smallest_coins_quantity_in_group = \
                user.learning_group.users\
                .aggregate(
                    smallest_coins_quantity=models.Min(
                        'hero__coins', output_field=models.DecimalField()
                    )
                )['smallest_coins_quantity']

            gifts_qs = gifts_qs.annotate(
                can_buy=models.Case(
                    models.When(
                        is_group_wide=False,
                        price__lte=user.hero.coins/Decimal(quantity),
                        then=True
                    ),
                    models.When(
                        is_group_wide=True,
                        price__lte=smallest_coins_quantity_in_group /
                        Decimal(quantity),
                        then=True
                    ),
                    default=False, output_field=models.BooleanField()
                )
            )

        return gifts_qs


class Gift(models.Model):
    hero_class = models.ForeignKey(
        'HeroClass', on_delete=models.SET_NULL, related_name='gifts',
        null=True,
    )

    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='gifts/', null=True, blank=True)
    remain = models.FloatField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=4)

    is_group_wide = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    objects = GiftsManager()

    def __str__(self):
        return self.name


class Cristal(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='cristal/', null=True, blank=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    cristal = models.OneToOneField(
        'Cristal', on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Rule(models.Model):
    name = models.CharField(max_length=500)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Gradation(models.Model):
    name = models.CharField(max_length=500)
    money = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    experience = models.FloatField()
    rule = models.ForeignKey(
        'Rule', on_delete=models.CASCADE, related_name='gradations'
    )

    def __str__(self):
        return self.name


class Penalty(models.Model):
    name = models.CharField(max_length=500)
    experience = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Penalties'
