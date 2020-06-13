import time
from datetime import timedelta
from unittest import mock

from django.conf import settings
from django.test import override_settings
from django.urls import reverse
from graphql_jwt.settings import jwt_settings
from helpers import generate_signature
from rest_framework.test import APITestCase
from graphql_jwt.testcases import JSONWebTokenTestCase

from tests.data_factories import UserFactory, SocialUserFactory


class BaseAuthTestCase(JSONWebTokenTestCase):
    plain_text_password = 'new password'

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(role='teacher')
        cls.user.set_password(cls.plain_text_password)
        cls.user.save()

    def _get_tokens_data(self, password, username=None):
        username = username or self.user.username
        mutation = '''
            mutation TokenAuth($username: String!, $password: String!) {
                tokenAuth(username: $username, password: $password) {
                    token
                    refreshToken
                    refreshExpiresIn
                }
            }
        '''

        variables = {
            'username': username,
            'password': password
        }

        return self.client.execute(mutation, variables)

    def _get_token(self, username, password=None):
        password = password or self.plain_text_password

        tokens_data = self._get_tokens_data(username=username,
                                            password=password)
        return tokens_data.data['tokenAuth']['token']

    def _make_my_user_query(self):
        query = '''
            query myUser {
                myUser {
                    username
                }
            }
        '''

        return self.client.execute(query)

    def _refresh_token(self, refresh_token):
        mutation = '''
            mutation RefreshToken($refreshToken: String!) {
                refreshToken(refreshToken: $refreshToken) {
                    token
                    refreshToken
                    refreshExpiresIn
                }
            }
        '''

        variables = {'refreshToken': refresh_token}

        return self.client.execute(mutation, variables)

    def set_token(self, token):
        self.client._credentials = {
            jwt_settings.JWT_AUTH_HEADER_NAME: '{0} {1}'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX,
                token
                )
        }
        print(self.client._credentials)


class UserAuthTestCase(BaseAuthTestCase):
    def test_get_tokens_with_right_credentials(self):
        response = self._get_tokens_data(password=self.plain_text_password)

        self.assertFalse(response.errors)
        self.assertTrue(response.data['tokenAuth'])

    def test_get_tokens_with_right_credentials_for_social_user(self):
        social_user = SocialUserFactory(code='12345', user=self.user)

        response = self._get_tokens_data(
            password=generate_signature(social_user), username=social_user.code
        )

        self.assertFalse(response.errors)
        self.assertTrue(response.data['tokenAuth'])

    def test_get_tokens_with_wrong_credentials(self):
        response = self._get_tokens_data(password=f'{self.plain_text_password}_wrong')

        self.assertTrue(response.errors)
        self.assertFalse(response.data['tokenAuth'])

    def test_get_login_required_data_with_valid_token(self):
        tokens_data = self._get_tokens_data(password=self.plain_text_password)
        token = tokens_data.data['tokenAuth']['token']

        self.set_token(token)
        response = self._make_my_user_query()
        self.assertFalse(response.errors)
        self.assertEqual(response.data['myUser']['username'], self.user.username)

    @override_settings()
    def test_get_login_required_data_with_expired_token(self):
        settings.GRAPHQL_JWT['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1)

        tokens_data = self._get_tokens_data(password=self.plain_text_password)
        token = tokens_data.data['tokenAuth']['token']
        self.set_token(token)

        time.sleep(5)

        response = self._make_my_user_query()
        self.assertTrue(response.errors)

    @override_settings()
    def test_refresh_with_actual_token(self):
        settings.GRAPHQL_JWT['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1)

        tokens_data = self._get_tokens_data(password=self.plain_text_password)
        refresh_token = tokens_data.data['tokenAuth']['refreshToken']

        time.sleep(5)

        response = self._refresh_token(refresh_token=refresh_token)
        self.assertFalse(response.errors)

        refreshed_token = response.data['refreshToken']['token']

        self.set_token(refreshed_token)
        response = self._make_my_user_query()
        self.assertFalse(response.errors)
        self.assertEqual(response.data['myUser']['username'], self.user.username)


@override_settings(
    GRAPHQL_JWT={
        'JWT_VERIFY_EXPIRATION': True,
        'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
        'JWT_EXPIRATION_DELTA': timedelta(seconds=1),
        'JWT_REFRESH_EXPIRATION_DELTA': timedelta(seconds=1),
    }
)
class ExpiredRefreshTokenTestCase(BaseAuthTestCase):
    def test_refresh_with_expired_token(self):
        tokens_data = self._get_tokens_data(password=self.plain_text_password)
        refresh_token = tokens_data.data['tokenAuth']['refreshToken']

        time.sleep(5)

        response = self._refresh_token(refresh_token=refresh_token)
        self.assertTrue(response.errors)


class VkSocialUserAuthTestCase(APITestCase):
    path = reverse('class_room:vk_auth')
    social_user_code = '1'

    def _make_request(self, valid=True, social_user_code=None):
        code = social_user_code or self.social_user_code
        with mock.patch('helpers.is_vk_signature_valid',
                        mock.Mock(return_value=valid)):
            return self.client.get(self.path+f'?vk_user_id={code}')

    def test_vk_payload_is_invalid(self):
        response = self._make_request(valid=False)
        self.assertEqual(400, response.status_code)

    def test_social_user_does_not_exist(self):
        response = self._make_request()
        self.assertEqual(403, response.status_code)

    def test_social_user_is_not_associated(self):
        SocialUserFactory(code=self.social_user_code)

        response = self._make_request()
        self.assertEqual(401, response.status_code)

    def test_social_user_is_associated(self):
        user = UserFactory(role='student')
        SocialUserFactory(code=self.social_user_code, user=user)

        response = self._make_request()
        self.assertEqual(200, response.status_code)
        self.assertIn('password', response.json().keys())
