import time
from datetime import timedelta

from django.conf import settings
from django.test import override_settings
from graphql_jwt.testcases import JSONWebTokenTestCase

from tests.data_factories import UserFactory


class BaseAuthTestCase(JSONWebTokenTestCase):
    plain_text_password = 'new password'

    def setUp(self):
        self.user = UserFactory(role='teacher')
        self.user.set_password(self.plain_text_password)
        self.user.save()

    def _get_tokens(self, password):
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
            'username': self.user.username,
            'password': password
        }

        return self.client.execute(mutation, variables)

    def _make_my_user_query(self, token=None):
        query = '''
            query myUser($token: String!) {
                myUser(token: $token) {
                    username
                }
            }
        '''

        variables = {'token': token}

        return self.client.execute(query, variables)

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


class UserAuthTestCase(BaseAuthTestCase):
    def test_get_tokens_with_right_credentials(self):
        response = self._get_tokens(password=self.plain_text_password)

        self.assertFalse(response.errors)
        self.assertTrue(response.data['tokenAuth'])

    def test_get_tokens_with_wrong_credentials(self):
        response = self._get_tokens(password=f'{self.plain_text_password}_wrong')

        self.assertTrue(response.errors)
        self.assertFalse(response.data['tokenAuth'])

    def test_get_login_required_data_with_valid_token(self):
        tokens_data = self._get_tokens(password=self.plain_text_password)
        token = tokens_data.data['tokenAuth']['token']

        response = self._make_my_user_query(token=token)
        self.assertFalse(response.errors)
        self.assertEqual(response.data['myUser']['username'], self.user.username)

    @override_settings()
    def test_get_login_required_data_with_expired_token(self):
        settings.GRAPHQL_JWT['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1)

        tokens_data = self._get_tokens(password=self.plain_text_password)
        token = tokens_data.data['tokenAuth']['token']

        time.sleep(5)

        response = self._make_my_user_query(token=token)
        self.assertTrue(response.errors)

    @override_settings()
    def test_refresh_with_actual_token(self):
        settings.GRAPHQL_JWT['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1)

        tokens_data = self._get_tokens(password=self.plain_text_password)
        refresh_token = tokens_data.data['tokenAuth']['refreshToken']

        time.sleep(5)

        response = self._refresh_token(refresh_token=refresh_token)
        self.assertFalse(response.errors)

        refreshed_token = response.data['refreshToken']['token']

        response = self._make_my_user_query(token=refreshed_token)
        self.assertFalse(response.errors)
        self.assertEqual(response.data['myUser']['username'], self.user.username)


@override_settings(
    GRAPHQL_JWT={
        'JWT_ALLOW_ARGUMENT': True,
        'JWT_VERIFY_EXPIRATION': True,
        'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
        'JWT_EXPIRATION_DELTA': timedelta(seconds=1),
        'JWT_REFRESH_EXPIRATION_DELTA': timedelta(seconds=1),
    }
)
class ExpiredRefreshTokenTestCase(BaseAuthTestCase):
    def test_refresh_with_expired_token(self):
        tokens_data = self._get_tokens(password=self.plain_text_password)
        refresh_token = tokens_data.data['tokenAuth']['refreshToken']

        time.sleep(5)

        response = self._refresh_token(refresh_token=refresh_token)
        self.assertTrue(response.errors)
