from faker import Faker
from rest_framework.test import APITestCase

import tests.data_factories as factory
from class_room import models as m


class GetSocialUserStatusTestCase(APITestCase):
    code = '12345'

    def test_new_user(self):
        response = self.client.get(f'/api/v1/status/{self.code}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'new')

    def test_pending_user(self):
        factory.SocialUserFactory(code=self.code)

        response = self.client.get(f'/api/v1/status/{self.code}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'pending')

    def test_user(self):
        user = factory.UserFactory()
        factory.SocialUserFactory(code=self.code, user=user)

        response = self.client.get(f'/api/v1/status/{self.code}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'user')

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
