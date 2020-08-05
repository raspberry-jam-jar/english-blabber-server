from abc import abstractmethod, ABC
from collections import namedtuple
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from game_flow.models import UserGift, UserHero
from game_skeleton.models import Gift


GiftMutationType = namedtuple('GiftMutationType', ['quantity_is_negative',
                                                   'gift_is_group_wide'])


def validate_price(context):
    if not context.gift_class.can_buy:
        raise ValidationError('You have not enough money to buy it')


def validate_availability(context):
    if not context.gift_class:
        raise ValidationError('You try to buy unavailable for the hero gift')


def validate_remains(context):
    if context.gift_class.remain is not None and \
            context.gift_class.remain < context.quantity:
        raise ValidationError(
            'You try to buy gift which has not enough remains'
        )


def validate_is_in_backpack(context):
    if not context.user_gift:
        raise ValidationError(
            'You try to use gift which is not in your backpack'
        )


def validate_quantity(context):
    if context.user_gift.quantity + context.quantity < 0:
        raise ValidationError('You try to use more then you have bought')


class GiftStrategy(ABC):
    validators = list()

    def __init__(self, gift_class_id, quantity, user_id):
        self.quantity = quantity
        self.hero = UserHero.objects.get(user_id=user_id)
        self.gift_class = \
            Gift.objects. \
            get_available(user=self.hero.user, quantity=self.quantity). \
            select_for_update(). \
            filter(id=gift_class_id).first()

    def validate(self):
        for validator in self.validators:
            validator(context=self)

    def run(self):
        self.validate()
        self.make_mutation()

    @abstractmethod
    def make_mutation(self):
        raise NotImplementedError

    @staticmethod
    def create(gift_class_id, quantity, user_id):
        gift_class = \
            Gift.objects.only('is_group_wide').get(id=gift_class_id)

        gift_mutation_type = GiftMutationType(
            quantity_is_negative=quantity < 0,
            gift_is_group_wide=gift_class.is_group_wide
        )

        gift_strategy = GIFT_STRATEGY_MAPPER[gift_mutation_type]
        return gift_strategy(gift_class_id=gift_class_id,
                             quantity=quantity, user_id=user_id)


class CommonUseGiftStrategy(GiftStrategy):
    validators = [validate_is_in_backpack, validate_quantity]

    def __init__(self, gift_class_id, quantity, user_id):
        super(CommonUseGiftStrategy, self).__init__(gift_class_id, quantity,
                                                    user_id)

        self.user_gift = \
            UserGift.objects.\
            select_for_update(). \
            filter(gift_class_id=gift_class_id,
                   hero=self.hero).\
            first()

    def make_mutation(self):
        # TODO write logic to use the group gift
        self.user_gift.quantity += self.quantity

        if not self.user_gift.quantity:
            self.user_gift.delete()
        else:
            self.user_gift.save()

        return self.user_gift


class CommonBuyGiftStrategy(GiftStrategy):
    def make_mutation(self):
        self.pay_for_gift()

        user_gift, created = \
            self.hero.gifts.get_or_create(gift_class_id=self.gift_class.id)
        if not created:
            user_gift.quantity += self.quantity
        else:
            user_gift.quantity = self.quantity
        user_gift.save()

        return user_gift

    def pay_for_gift(self):
        pass


class BuyGroupGiftStrategy(CommonBuyGiftStrategy):
    validators = [validate_availability, validate_price]

    def pay_for_gift(self):
        # TODO проверить, что уровень пользователя позволяет покупать
        #  групповые подарки
        UserHero.objects. \
            filter(user__learning_groups__in=self.hero.user.learning_groups,
                   user__role='student'). \
            update(
                coins=models.F('coins') -
                Decimal(self.quantity)*self.gift_class.price
            )


class BuyGiftStrategy(CommonBuyGiftStrategy):
    validators = [validate_availability, validate_price, validate_remains]

    def pay_for_gift(self):
        self.hero.coins -= self.gift_class.price * Decimal(self.quantity)
        self.hero.save()


GIFT_STRATEGY_MAPPER = {
    GiftMutationType(quantity_is_negative=True, gift_is_group_wide=True):
        CommonUseGiftStrategy,
    GiftMutationType(quantity_is_negative=True, gift_is_group_wide=False):
        CommonUseGiftStrategy,
    GiftMutationType(quantity_is_negative=False, gift_is_group_wide=True):
        BuyGroupGiftStrategy,
    GiftMutationType(quantity_is_negative=False, gift_is_group_wide=False):
        BuyGiftStrategy
}
