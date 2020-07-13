import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from django.db import transaction

from decorators import student_or_staff_member_required
from game_flow.gift_strategies import GiftStrategy
from game_flow.models import UserGift, UserHero
from game_skeleton.models import HeroSkill, HeroClass


class HeroSkillType(DjangoObjectType):
    class Meta:
        model = HeroSkill


class HeroClassType(DjangoObjectType):
    level = graphene.Int()
    skills = graphene.List(of_type=HeroSkillType)

    class Meta:
        model = HeroClass

    def resolve_skills(self, info):
        return HeroSkill.objects.filter(id__in=self.skill_ids)

    def resolve_level(self, info):
        return self.id


class BoughtGiftType(DjangoObjectType):
    name = graphene.String()
    price = graphene.Float()
    image = graphene.String()

    class Meta:
        model = UserGift
        fields = '__all__'

    gift_class_name = graphene.String()

    def resolve_name(self, info):
        return getattr(self, 'name', None)

    def resolve_price(self, info):
        return getattr(self, 'price', None)

    def resolve_image(self, info):
        return getattr(self, 'image', None)


class UserHeroType(DjangoObjectType):
    class Meta:
        model = UserHero

    backpack = graphene.List(BoughtGiftType)

    def resolve_backpack(self, info):
        return UserGift.objects.\
            filter(hero=self).\
            order_by('datetime_edited', 'gift_class__price',
                     'gift_class__name')


class BuyOrUseUserGiftMutation(graphene.Mutation):
    class Arguments:
        gift_class_id = graphene.Int(required=True)
        quantity = graphene.Int(required=True)
        user_id = graphene.Int()

    user_gift = graphene.Field(BoughtGiftType)

    @login_required
    @student_or_staff_member_required
    @transaction.atomic
    def mutate(self, info, gift_class_id, quantity, user_id, **kwargs):
        gift_strategy = GiftStrategy.create(gift_class_id, quantity, user_id)
        return gift_strategy.run()


class Query(graphene.ObjectType):
    hero_backpack = graphene.List(BoughtGiftType, user_id=graphene.Int())

    @login_required
    @student_or_staff_member_required
    def resolve_hero_backpack(self, info, user_id, **kwargs):
        hero = UserHero.objects.get(user_id=user_id)
        return UserGift.objects.\
            filter(hero=hero).\
            order_by('datetime_edited', 'gift_class__price',
                     'gift_class__name')
