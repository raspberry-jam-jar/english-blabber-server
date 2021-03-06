from faker import Faker
from graphql_jwt.testcases import JSONWebTokenTestCase
from rest_framework.test import APITestCase

from class_room import models as cm
from game_skeleton import models as gm
from tests.data_factories import UserFactory


class GetSocialUserStatusTestCase(APITestCase):
    code = '12345'

    def test_apply_to_join(self):
        data = {
            'code': self.code,
            'first_name': Faker().first_name(),
            'last_name': Faker().last_name()
        }

        response = self.client.post('/api/v1/apply/', data=data,
                                    format='json')
        self.assertEqual(response.status_code, 201)

        social_users_qs = \
            cm.SocialUser.objects.filter(code=self.code, platform='vk')

        self.assertEqual(1, social_users_qs.count())

        response = self.client.post('/api/v1/apply/', data=data,
                                    format='json')
        self.assertEqual(response.status_code, 200)


class GetGiftsTestCase(JSONWebTokenTestCase):
    plain_text_password = 'new password'

    @classmethod
    def setUpTestData(cls):
        cls.student = UserFactory(role='student')
        cls.teacher = UserFactory(role='teacher', is_staff=True)

        for user in (cls.student, cls.teacher):
            user.set_password(cls.plain_text_password)
            user.save()

        cls.student.hero.coins = 100
        cls.student.hero.save()
            
    def setUp(self) -> None:
        self.client.authenticate(self.student)

    def _execute_available_gifts_query(self):
        query = '''
            query availableGifts {
                availableGifts {
                    name
                    price
                    isGroupWide
                    remain
                    canBuy
                }
            }
        '''

        return self.client.execute(query)

    def _execute_available_for_user_gifts_query(self, user_id):
        query = '''
            query availableGifts($userId:Int!){
                availableGifts(userId: $userId) {
                    name
                    price
                    isGroupWide
                    remain
                    canBuy
                }
            }
        '''
        variables = {'userId': user_id, }
        return self.client.execute(query, variables)

    def _execute_buy_or_use_gift_mutation(self, gift_class_id, quantity):
        mutation = '''
            mutation BuyOrUseUserGiftMutation($giftClassId:Int!, $quantity:Int!){
                buyOrUseGift(giftClassId: $giftClassId, quantity: $quantity){
                    userGift {
                        id
                    }
                }
            }
        '''

        variables = {'giftClassId': gift_class_id, 'quantity': quantity}
        return self.client.execute(mutation, variables)
    
    def _execute_buy_or_use_gift_for_user_mutation(self, gift_class_id, quantity, 
                                                   user_id):
        mutation = '''
            mutation BuyOrUseUserGiftMutation($giftClassId:Int!, $quantity:Int!, 
                                              $userId:Int!) {
                buyOrUseGift(giftClassId: $giftClassId, quantity: $quantity,
                             userId: $userId,) {
                    userGift {
                        id
                    }
                }
            }
        '''

        variables = {'giftClassId': gift_class_id,
                     'quantity': quantity, 'userId': user_id}
        return self.client.execute(mutation, variables)

    def _execute_hero_backpack_query(self):
        query = '''
        query HeroBackpack {
                heroBackpack {
                    name
                    quantity
                }
            }
        '''

        return self.client.execute(query)

    def _execute_my_user_query(self):
        query = '''
        query {
            myUser{
                hero {
                    heroClass {
                        capacity
                        name
                        level
                        skills {
                            name
                        }
                    }
                }
            }
        }
        '''

        return self.client.execute(query)

    def test_get_user_hero_info(self):
        response = self._execute_my_user_query()
        hero_class = response.data['myUser']['hero']['heroClass']

        self.assertEqual(
            hero_class['name'], self.student.hero.hero_class.name
        )
        self.assertEqual(
            hero_class['level'], self.student.hero.hero_class.id
        )

        self.assertCountEqual(
            hero_class['skills'],
            gm.HeroSkill.objects.
            filter(id__in=self.student.hero.hero_class.skill_ids).
            values('name')
        )
    
    def buy_or_use_available_gift(self, quantity, user=None, gift_class=None):
        if not gift_class:
            gift_class = \
                gm.Gift.objects. \
                exclude(hero_class_id__gt=self.student.hero.hero_class_id). \
                exclude(is_group_wide=True). \
                first()

        if not user:
            return self._execute_buy_or_use_gift_mutation(
                gift_class_id=gift_class.id, quantity=quantity,
            )
        return self._execute_buy_or_use_gift_for_user_mutation(
            gift_class_id=gift_class.id, quantity=quantity,
            user_id=self.student.id
        )

    def test_get_available_student_gifts(self):
        response = self._execute_available_gifts_query()
        self.assertFalse(response.errors)

    def test_get_available_student_gifts_without_login(self):
        self.client.logout()
        response = self._execute_available_gifts_query()
        self.assertTrue(response.errors)

    def test_attempt_to_get_available_for_user_gifts_by_student(self):
        response = self._execute_available_for_user_gifts_query(
            user_id=self.student.id,
        )
        self.assertTrue(response.errors)
        self.assertEqual(
            'You do not have permission to perform this action',
            response.errors[0].message
        )

    def test_attempt_to_get_available_for_user_gifts_by_teacher(self):
        self.client.authenticate(self.teacher)
        response = self._execute_available_for_user_gifts_query(
            user_id=self.student.id,
        )
        self.assertFalse(response.errors)

    def test_buy_unavailable_for_hero_gift_by_student(self):
        unavailable_gift_class = \
            gm.Gift.objects.\
            filter(hero_class_id__gt=self.student.hero.hero_class_id).\
            exclude(is_group_wide=True).\
            first()

        response = self._execute_buy_or_use_gift_mutation(
            gift_class_id=unavailable_gift_class.id, quantity=1
        )
        self.assertTrue(response.errors)
        self.assertEqual(
            'You try to buy unavailable for the hero gift',
            response.errors[0].original_error.args[0]
        )

        response = self._execute_hero_backpack_query()
        self.assertFalse(response.data['heroBackpack'])

    def test_buy_too_expensive_gift_by_student(self):
        self.student.hero.coins = 0
        self.student.hero.save()

        some_too_expensive_gift_class = \
            gm.Gift.objects. \
            filter(hero_class_id__lte=self.student.hero.hero_class_id). \
            exclude(is_group_wide=True). \
            exclude(price=0). \
            first()

        response = self._execute_buy_or_use_gift_mutation(
            gift_class_id=some_too_expensive_gift_class.id, quantity=1
        )

        self.assertTrue(response.errors)
        self.assertEqual(
            'You have not enough money to buy it',
            response.errors[0].original_error.args[0]
        )

    def test_buy_not_enough_remains_gift_by_student(self):
        some_zero_remains_gift_class = \
            gm.Gift.objects. \
            filter(hero_class_id__lte=self.student.hero.hero_class_id, remain=0). \
            first()

        response = self._execute_buy_or_use_gift_mutation(
            gift_class_id=some_zero_remains_gift_class.id, quantity=1
        )

        self.assertTrue(response.errors)
        self.assertEqual(
            'You try to buy gift which has not enough remains',
            response.errors[0].original_error.args[0]
        )

    def test_buy_available_personal_gift_by_student(self):
        gift_quantity_to_buy = 2

        some_available_gift_class = \
            gm.Gift.objects. \
            exclude(hero_class_id__gt=self.student.hero.hero_class_id). \
            exclude(is_group_wide=True). \
            first()

        expected_decreased_hero_coins = \
            self.student.hero.coins - \
            some_available_gift_class.price*gift_quantity_to_buy

        response = self.buy_or_use_available_gift(
            quantity=gift_quantity_to_buy, gift_class=some_available_gift_class
        )

        self.student.refresh_from_db()

        self.assertFalse(response.errors)
        self.assertEqual(
            expected_decreased_hero_coins,
            self.student.hero.coins
        )

        response = self._execute_hero_backpack_query()

        self.assertEqual(len(response.data['heroBackpack']), 1)
        self.assertDictEqual(
            response.data['heroBackpack'][0],
            {'name': some_available_gift_class.name, 'quantity': 2}
        )

        response = self._execute_buy_or_use_gift_mutation(
            gift_class_id=some_available_gift_class.id, quantity=1,
        )
        self.assertFalse(response.errors)

        response = self._execute_hero_backpack_query()
        self.assertEqual(len(response.data['heroBackpack']), 1)
        self.assertDictEqual(
            response.data['heroBackpack'][0],
            {'name': some_available_gift_class.name, 'quantity': 3}
        )

    def test_attempt_to_use_unavailable_gift_by_student(self):
        some_unavailable_gift_class = \
            gm.Gift.objects. \
            filter(hero_class_id__gt=self.student.hero.hero_class_id). \
            exclude(is_group_wide=True). \
            first()

        response = self.buy_or_use_available_gift(
            quantity=1, gift_class=some_unavailable_gift_class
        )
        self.assertTrue(response.errors)

        response = self._execute_hero_backpack_query()
        self.assertFalse(response.data['heroBackpack'])

    def test_attempt_to_use_absent_in_backpack_gift_by_student(self):
        response = self.buy_or_use_available_gift(quantity=-1)

        self.assertTrue(response.errors)

    def test_attempt_to_use_bought_gift_by_student(self):
        response = self.buy_or_use_available_gift(quantity=1)
        self.assertFalse(response.errors)
        response = self.buy_or_use_available_gift(quantity=-1)
        self.assertFalse(response.errors)

        response = self._execute_hero_backpack_query()
        self.assertFalse(response.data['heroBackpack'])

    def test_attempt_to_use_bought_gift_for_user_by_student(self):
        another_student = UserFactory(role='student')

        response = self.buy_or_use_available_gift(quantity=1, user=another_student)
        self.assertTrue(response.errors)
        self.assertEqual(
            'You do not have permission to perform this action',
            response.errors[0].message
        )

    def test_attempt_to_use_bought_gift_for_user_by_teacher(self):
        self.client.authenticate(self.teacher)
        response = self.buy_or_use_available_gift(quantity=1,
                                                  user=self.student)
        self.assertFalse(response.errors)

        self.client.authenticate(self.student)
        response = self._execute_hero_backpack_query()
        self.assertEqual(len(response.data['heroBackpack']), 1)


class TeacherDashboardTestCase(JSONWebTokenTestCase):
    @classmethod
    def setUpTestData(cls):
        students = UserFactory.create_batch(role='student', size=5)
        cls.student = students[0]
        cls.teacher = UserFactory(role='teacher', is_staff=True)

        cls._create_learning_group(
            description='first learning group',
            participants=(students[0], students[1], cls.teacher)
        )

        cls._create_learning_group(
            description='second learning group',
            participants=(students[2], students[3], cls.teacher)
        )

        cls._create_learning_group(
            description='third learning group',
            participants=(students[4], )
        )

        cls.some_gradation = gm.Gradation.objects.order_by('-experience').first()

    @staticmethod
    def _create_learning_group(description, participants):
        some_learning_group = \
            cm.LearningGroup.objects.create(description=description)
        some_learning_group.users.add(*participants)

    def setUp(self) -> None:
        self.client.authenticate(self.teacher)

    def _execute_learning_groups_query(self):
        query = '''
            query learningGroups {
                learningGroups {
                    description
                    users {
                        id
                        role
                    }
                }
            }
        '''

        return self.client.execute(query)

    def _execute_skills_query(self):
        query = '''
            query skills {
                skills {
                    name
                    rules {
                        name
                        gradations {
                            name
                            money
                            experience
                        }
                    }
                }
            }
        '''

        return self.client.execute(query)

    def _execute_add_skills_mutation(self, gradation_id, user_id):
        mutation = '''
            mutation AddSkills($gradationId:Int!, $userId:Int!) {
                addSkills(gradationId: $gradationId, userId: $userId) {
                    hero {
                        coins
                        capacity
                        heroClass {
                            level
                        }
                    }
                }
            }
        '''

        variables = {'gradationId': gradation_id,
                     'userId': user_id}
        return self.client.execute(mutation, variables)

    def test_get_groups_list(self):
        response = self._execute_learning_groups_query()

        self.assertFalse(response.errors)
        self.assertEqual(2, len(response.data['learningGroups']))

    def test_get_skills_list(self):
        response = self._execute_skills_query()

        self.assertFalse(response.errors)

    def test_add_skills(self):
        response = self._execute_add_skills_mutation(
            gradation_id=self.some_gradation.id,
            user_id=self.student.id
        )

        self.assertFalse(response.errors)
        self.student.refresh_from_db()
        self.assertEqual(self.some_gradation.money, self.student.hero.coins)
        self.assertEqual(self.some_gradation.experience,
                         self.student.hero.capacity)

    def test_hero_level_upgrade(self):
        current_hero_level = self.student.hero.hero_class.id
        some_coins = 10
        expected_coins = some_coins + self.some_gradation.money
        self.student.hero.capacity = \
            self.student.hero.hero_class.capacity - \
            self.some_gradation.experience / 2
        self.student.hero.coins = some_coins
        self.student.hero.save()

        response = self._execute_add_skills_mutation(
            gradation_id=self.some_gradation.id,
            user_id=self.student.id
        )

        self.assertFalse(response.errors)
        self.student.refresh_from_db()
        self.assertEqual(expected_coins, self.student.hero.coins)
        self.assertEqual(self.some_gradation.experience / 2,
                         self.student.hero.capacity)
        self.assertEqual(current_hero_level + 1,
                         self.student.hero.hero_class.id)

    def test_hero_level_upgrade_for_last_hero_class(self):
        final_hero_class = gm.HeroClass.objects.order_by('-id').first()
        self.student.hero.hero_class = final_hero_class
        self.student.hero.capacity = \
            self.student.hero.hero_class.capacity - \
            self.some_gradation.experience / 2
        self.student.hero.save()

        response = self._execute_add_skills_mutation(
            gradation_id=self.some_gradation.id,
            user_id=self.student.id
        )

        self.assertFalse(response.errors)
        self.student.refresh_from_db()
        self.assertEqual(final_hero_class.capacity,
                         self.student.hero.capacity)
