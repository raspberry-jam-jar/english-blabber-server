from django.db import models
from django.test import TestCase

from class_room.models import LearningGroup
from game_flow.models import UserHero
from game_skeleton.models import Gift
from tests.data_factories import UserFactory


class GiftTestCase(TestCase):
    minimal_gift_price = 10

    def setUp(self) -> None:
        self.student = UserFactory(role='student')

    def test_available_gifts_for_base_hero_no_group(self):
        """
        Test available gifts for student user which is not associated
        with any learning group.

        Expected result:
        - gifts hero classes match user hero class
        - group gifts are not in the query

        :return:
        """

        available_gifts = Gift.objects.get_available(self.student)
        self.assertCountEqual(
            available_gifts.values_list('hero_class_id', flat=True).distinct(),
            (self.student.hero.hero_class_id, )
        )
        self.assertFalse(available_gifts.filter(is_group_wide=True).exists())

    def test_can_buy_attribute_for_advanced_hero_no_group(self):
        """
        Test the `can_buy` attribute for student user which is not associated
        with any learning group.

        Expected result: student can buy the non-group gift if his/her hero have
        more or equal coins to the gift price.

        :return:
        """
        self.student.hero.hero_class_id = 2
        self.student.hero.save()

        available_gifts = Gift.objects.get_available(self.student)
        self.assertFalse(available_gifts.filter(can_buy=True).exists())

        self.student.hero.coins = self.minimal_gift_price
        self.student.hero.save()

        available_gifts = Gift.objects.get_available(self.student)

        self.assertTrue(available_gifts.filter(can_buy=True).exists())
        self.assertTrue(available_gifts.filter(can_buy=False).exists())

        for available_gift in available_gifts:
            if available_gift.price > self.student.hero.coins:
                self.assertFalse(available_gift.can_buy)
            else:
                self.assertTrue(available_gift.can_buy)

    def test_group_gifts(self):
        """
        Test group gifts attributes for student user with a learning group.

        Expected result:
        - student can buy the group gift if it can be bought by the student
        with the smallest coins quantity in the group

        :return:
        """

        some_learning_group = LearningGroup.objects.create(description='First group')

        self.student.learning_group = some_learning_group
        self.student.save()

        self.student.hero.coins = self.minimal_gift_price
        self.student.hero.save()

        another_student = \
            UserFactory(role='student', learning_group=some_learning_group)

        available_gifts = Gift.objects.get_available(self.student)
        self.assertTrue(available_gifts.filter(is_group_wide=True).exists())
        self.assertFalse(
            available_gifts.filter(is_group_wide=True).
            exclude(can_buy=False).
            exists()
        )

        another_student.hero.coins = self.minimal_gift_price
        another_student.hero.save()

        new_available_gifts = Gift.objects.get_available(self.student)

        average_coins_quantity = \
            UserHero.objects. \
            filter(user__learning_group=some_learning_group). \
            aggregate(models.Avg('coins'))['coins__avg']

        for available_group_gift in new_available_gifts.filter(is_group_wide=True):
            if available_group_gift.price > average_coins_quantity:
                self.assertFalse(available_group_gift.can_buy)
            else:
                self.assertTrue(available_group_gift.can_buy)
