from faker import Faker
from rest_framework.test import APITestCase

from class_room import models as cm
from game_skeleton import models as gm
from tests.data_factories import UserFactory
from tests.test_auth_api import BaseAuthTestCase


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
        self.assertEqual(response.status_code, 400)


class GetGiftsTestCase(BaseAuthTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = UserFactory(role='student')
        cls.teacher = UserFactory(role='teacher', is_staff=True)

        for user in (cls.student, cls.teacher):
            user.set_password(cls.plain_text_password)
            user.save()
            
    def setUp(self) -> None:
        self.student_token = self._get_token(username=self.student.username,
                                             password=self.plain_text_password)

    def _execute_available_gifts_query(self, token):
        query = '''
            query availableGifts($token: String!){
                availableGifts(token: $token) {
                    name
                    price
                    isGroupWide
                    remain
                    canBuy
                }
            }
        '''
        variables = {'token': token}
        return self.client.execute(query, variables)

    def _execute_available_for_user_gifts_query(self, user_id, token):
        query = '''
            query availableGifts($userId:Int!, $token: String!){
                availableGifts(userId: $userId, token: $token) {
                    name
                    price
                    isGroupWide
                    remain
                    canBuy
                }
            }
        '''
        variables = {'userId': user_id, 'token': token}
        return self.client.execute(query, variables)

    def _execute_buy_or_use_gift_mutation(self, gift_class_id, quantity, token):
        mutation = '''
            mutation BuyOrUseUserGiftMutation($giftClassId:Int!, $quantity:Float!, 
                                              $token: String!) {
                buyOrUseGift(giftClassId: $giftClassId, quantity: $quantity,
                             token: $token) {
                    userGift {
                        id
                    }
                }
            }
        '''

        variables = {'giftClassId': gift_class_id, 'token': token,
                     'quantity': quantity}
        return self.client.execute(mutation, variables)
    
    def _execute_buy_or_use_gift_for_user_mutation(self, gift_class_id, quantity, 
                                                   token, user_id):
        mutation = '''
            mutation BuyOrUseUserGiftMutation($giftClassId:Int!, $quantity:Float!, 
                                              $token: String!, $userId:Int!) {
                buyOrUseGift(giftClassId: $giftClassId, quantity: $quantity,
                             token: $token, userId: $userId,) {
                    userGift {
                        id
                    }
                }
            }
        '''

        variables = {'giftClassId': gift_class_id, 'token': token,
                     'quantity': quantity, 'userId': user_id}
        return self.client.execute(mutation, variables)

    def _execute_hero_backpack_query(self, token):
        query = '''
        query HeroBackpack($token: String!){
                heroBackpack(token: $token) {
                    giftClassName
                    quantity
                }
            }
        '''

        variables = {'token': token}
        return self.client.execute(query, variables)
    
    def buy_or_use_available_gift(self, quantity, token, user=None, gift_class=None):
        if not gift_class:
            gift_class = \
                gm.Gift.objects. \
                exclude(hero_class_id__gt=self.student.hero.hero_class_id). \
                exclude(is_group_wide=True). \
                first()
        
        if not user:
            return self._execute_buy_or_use_gift_mutation(
                gift_class_id=gift_class.id, quantity=quantity,
                token=token
            )
        return self._execute_buy_or_use_gift_for_user_mutation(
            gift_class_id=gift_class.id, quantity=quantity,
            token=token, user_id=self.student.id
        )

    def test_get_available_student_gifts(self):
        response = self._execute_available_gifts_query(token=self.student_token)
        self.assertFalse(response.errors)

    def test_get_available_student_gifts_with_invalid_token(self):
        response = self._execute_available_gifts_query(token='gfwif7gd')
        self.assertTrue(response.errors)

    def test_attempt_to_get_available_for_user_gifts_by_student(self):
        response = self._execute_available_for_user_gifts_query(
            user_id=self.student.id, token=self.student_token
        )
        self.assertTrue(response.errors)
        self.assertEqual(
            'You do not have permission to perform this action',
            response.errors[0].message
        )

    def test_attempt_to_get_available_for_user_gifts_by_teacher(self):
        teacher_token = self._get_token(username=self.teacher.username,
                                        password=self.plain_text_password)

        response = self._execute_available_for_user_gifts_query(
            user_id=self.student.id, token=teacher_token
        )
        self.assertFalse(response.errors)

    def test_buy_unavailable_gift_by_student(self):
        unavailable_gift_class = \
            gm.Gift.objects.\
            filter(hero_class_id__gt=self.student.hero.hero_class_id).\
            exclude(is_group_wide=True).\
            first()

        response = self._execute_buy_or_use_gift_mutation(
            gift_class_id=unavailable_gift_class.id, quantity=1, 
            token=self.student_token
        )
        self.assertTrue(response.errors)

        response = self._execute_hero_backpack_query(token=self.student_token)
        self.assertFalse(response.data['heroBackpack'])

    def test_buy_available_gift_by_student(self):
        some_available_gift_class = \
            gm.Gift.objects. \
            exclude(hero_class_id__gt=self.student.hero.hero_class_id). \
            exclude(is_group_wide=True). \
            first()
        response = self.buy_or_use_available_gift(
            quantity=2, token=self.student_token,
            gift_class=some_available_gift_class
        )
        self.assertFalse(response.errors)

        response = self._execute_hero_backpack_query(token=self.student_token)
        self.assertEqual(len(response.data['heroBackpack']), 1)
        self.assertDictEqual(
            response.data['heroBackpack'][0],
            {'giftClassName': some_available_gift_class.name, 'quantity': 2}
        )

        response = self._execute_buy_or_use_gift_mutation(
            gift_class_id=some_available_gift_class.id, quantity=1, 
            token=self.student_token
        )
        self.assertFalse(response.errors)

        response = self._execute_hero_backpack_query(token=self.student_token)
        self.assertEqual(len(response.data['heroBackpack']), 1)
        self.assertDictEqual(
            response.data['heroBackpack'][0],
            {'giftClassName': some_available_gift_class.name, 'quantity': 3}
        )

    def test_attempt_to_use_unavailable_gift_by_student(self):
        some_unavailable_gift_class = \
            gm.Gift.objects. \
            filter(hero_class_id__gt=self.student.hero.hero_class_id). \
            exclude(is_group_wide=True). \
            first()

        response = self.buy_or_use_available_gift(
            quantity=1, token=self.student_token,
            gift_class=some_unavailable_gift_class
        )
        self.assertTrue(response.errors)

        response = self._execute_hero_backpack_query(token=self.student_token)
        self.assertFalse(response.data['heroBackpack'])

    def test_attempt_to_use_absent_in_backpack_gift_by_student(self):
        response = self.buy_or_use_available_gift(quantity=-1,
                                                  token=self.student_token)

        self.assertTrue(response.errors)

    def test_attempt_to_use_bought_gift_by_student(self):
        response = self.buy_or_use_available_gift(quantity=1, token=self.student_token)
        self.assertFalse(response.errors)
        response = self.buy_or_use_available_gift(quantity=-1,
                                                  token=self.student_token)
        self.assertFalse(response.errors)

        response = self._execute_hero_backpack_query(token=self.student_token)
        self.assertFalse(response.data['heroBackpack'])

    def test_attempt_to_use_bought_gift_for_user_by_student(self):
        another_student = UserFactory(role='student')

        response = self.buy_or_use_available_gift(quantity=1, user=another_student,
                                                  token=self.student_token)
        self.assertTrue(response.errors)
        self.assertEqual(
            'You do not have permission to perform this action',
            response.errors[0].message
        )

    def test_attempt_to_use_bought_gift_for_user_by_teacher(self):
        teacher_token = self._get_token(username=self.teacher.username,
                                        password=self.plain_text_password)
        response = self.buy_or_use_available_gift(quantity=1, token=teacher_token,
                                                  user=self.student)
        self.assertFalse(response.errors)

        response = self._execute_hero_backpack_query(token=self.student_token)
        self.assertEqual(len(response.data['heroBackpack']), 1)
