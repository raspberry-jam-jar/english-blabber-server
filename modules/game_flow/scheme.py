import graphene
from django.core.exceptions import ValidationError

from django.db import models, transaction
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from class_room.models import User
from decorators import student_or_staff_member_required
from game_flow.models import UserGift, UserHero
from game_skeleton.models import Gift


class UserGiftType(DjangoObjectType):
    class Meta:
        model = UserGift

    gift_class_name = graphene.String()

    def resolve_gift_class_name(self, info):
        return self.gift_class.name


class UserHeroType(DjangoObjectType):
    class Meta:
        model = UserHero

    hero_class_name = graphene.String()
    hero_class_level = graphene.Int()
    backpack = graphene.List(UserGiftType)

    def resolve_hero_class_name(self, info):
        return self.hero_class.name

    def resolve_hero_class_level(self, info):
        return self.hero_class.id

    def resolve_backpack(self, info):
        return UserGift.objects.\
            filter(hero=self).\
            order_by('datetime_edited', 'gift_class__price',
                     'gift_class__name')


class BuyOrUseUserGiftMutation(graphene.Mutation):
    class Arguments:
        gift_class_id = graphene.Int(required=True)
        quantity = graphene.Float(required=True)
        user_id = graphene.Int()

    user_gift = graphene.Field(UserGiftType)

    @staticmethod
    def _validate_availability(user_id, gift_class_id):
        available_gift_classes_ids = \
            Gift.objects. \
            get_available(user=User.objects.get(id=user_id)). \
            values_list('id', flat=True)

        if gift_class_id not in available_gift_classes_ids:
            raise ValidationError(
                'You try to buy unavailable for the hero gift'
            )

    @staticmethod
    def _validate_is_in_backpack(quantity, user_gift_qs):
        if quantity > 0:
            return

        if not user_gift_qs:
            raise ValidationError(
                'You try to use gift which is not in your backpack'
            )

    @staticmethod
    def _validate_quantity(quantity, user_gift_qs):
        if user_gift_qs.first().quantity + quantity < 0:
            raise ValidationError('You try to use more then you have bought')

    @login_required
    @student_or_staff_member_required
    @transaction.atomic
    def mutate(self, info, gift_class_id, quantity, user_id, **kwargs):
        # TODO add buy group gift

        BuyOrUseUserGiftMutation._validate_availability(
            user_id=user_id, gift_class_id=gift_class_id
        )
        hero = UserHero.objects.get(user_id=user_id)
        user_gift_qs = \
            UserGift.objects.select_for_update().\
            filter(gift_class_id=gift_class_id, hero=hero)

        BuyOrUseUserGiftMutation._validate_is_in_backpack(
            user_gift_qs=user_gift_qs, quantity=quantity
        )
        if not user_gift_qs:
            user_gift = UserGift.objects.create(gift_class_id=gift_class_id,
                                                hero=hero, quantity=quantity)
            return BuyOrUseUserGiftMutation(user_gift)

        BuyOrUseUserGiftMutation._validate_quantity(user_gift_qs=user_gift_qs,
                                                    quantity=quantity)
        user_gift_qs.update(quantity=models.F('quantity')+quantity)
        if not user_gift_qs.first().quantity:
            user_gift_qs.delete()

        return BuyOrUseUserGiftMutation(user_gift_qs.first())


class Query(graphene.ObjectType):
    hero_backpack = graphene.List(UserGiftType, user_id=graphene.Int())

    @login_required
    @student_or_staff_member_required
    def resolve_hero_backpack(self, info, user_id, **kwargs):
        hero = UserHero.objects.get(user_id=user_id)
        return UserGift.objects.\
            filter(hero=hero).\
            order_by('datetime_edited', 'gift_class__price',
                     'gift_class__name')
