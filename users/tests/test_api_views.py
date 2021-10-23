from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
)
from rest_framework.test import APIClient


class TestUsersViews(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username='test', password='testing123')

    def test_obtain_jwt(self):
        response = self.client.post('/api/auth/token/', {
            'username': 'test',
            'password': 'testing123'
        })
        res_json = response.json()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('access', res_json)
        self.assertIn('refresh', res_json)

    def test_obtain_jwt_missing_fields(self):
        response = self.client.post('/api/auth/token/', {
            'username': 'test',
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['This field is required.']})

    def test_obtain_jwt_user_not_found(self):
        response = self.client.post('/api/auth/token/', {
            'username': 'nouser',
            'password': 'nouser123'
        })
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'No active account found with the given credentials'})

    def test_refresh_jwt(self):
        res_get_token = self.client.post('/api/auth/token/', data={
            'username': 'test',
            'password': 'testing123',
        }).json()
        access, refresh = res_get_token['access'], res_get_token['refresh']

        res_refresh_token = self.client.post('/api/auth/token/refresh/', data={
            'refresh': refresh
        })
        self.assertEqual(res_refresh_token.status_code, HTTP_200_OK)

        data = res_refresh_token.json()
        self.assertIn('access', data)
        self.assertNotEqual(access, data['access'])

    def test_refresh_jwt_missing_fields(self):
        response = self.client.post('/api/auth/token/refresh/', {})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'refresh': ['This field is required.']})

    def test_refresh_jwt_invalid_refresh(self):
        response = self.client.post('/api/auth/token/refresh/', {
            'refresh': 'blablablablabla'
        })
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Token is invalid or expired', 'code': 'token_not_valid'})

    def test_verify_jwt(self):
        res_get_token = self.client.post('/api/auth/token/', data={
            'username': 'test',
            'password': 'testing123',
        }).json()
        access, refresh = res_get_token['access'], res_get_token['refresh']

        res_verify_access = self.client.post('/api/auth/token/verify/', {
            'token': access
        })
        self.assertEqual(res_verify_access.status_code, HTTP_200_OK)
        self.assertEqual(res_verify_access.json(), {})

        res_verify_refresh = self.client.post('/api/auth/token/verify/', {
            'token': refresh
        })
        self.assertEqual(res_verify_refresh.status_code, HTTP_200_OK)
        self.assertEqual(res_verify_refresh.json(), {})

    def test_verify_jwt_missing_fields(self):
        response = self.client.post('/api/auth/token/verify/', {})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'token': ['This field is required.']})

    def test_verify_jwt_token_invalid(self):
        response = self.client.post('/api/auth/token/verify/', {
            'token': 'totally_legit_jwt_xd'
        })
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Token is invalid or expired', 'code': 'token_not_valid'})
