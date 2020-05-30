from faker import Faker
from rest_framework.test import APITestCase

from class_room import models as m
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
            m.SocialUser.objects.filter(code=self.code, platform='vk')

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
            query availableForUserGifts($userId:Int!, $token: String!){
                availableForUserGifts(userId: $userId, token: $token) {
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

    def test_get_available_student_gifts(self):
        student_token = self._get_token(username=self.student.username,
                                        password=self.plain_text_password)

        response = self._execute_available_gifts_query(token=student_token)
        self.assertFalse(response.errors)

    def test_get_available_student_gifts_with_invalid_token(self):
        response = self._execute_available_gifts_query(token='gfwif7gd')
        self.assertTrue(response.errors)

    def test_attempt_to_get_available_for_user_gifts_by_student(self):
        student_token = self._get_token(username=self.student.username,
                                        password=self.plain_text_password)

        response = self._execute_available_for_user_gifts_query(
            user_id=self.student.id, token=student_token
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
