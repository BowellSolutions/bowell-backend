"""
Copyright (c) 2022 Adam Lisichin, Hubert Decyusz, Wojciech Nowicki, Gustaw Daczkowski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

author: Hubert Decyusz, Adam Lisichin

description: File contains tests used for users app testing.
"""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
)
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from users.serializers import UserSerializer, RegisterUserSerializer
from users.utils import get_tokens_for_user

User = get_user_model()


class TestUsersViews(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls) -> None:
        # noinspection PyUnresolvedReferences
        cls.user = User.objects.create_user(
            email='test@gmail.com', password='testing123',
            first_name='te', last_name='st', type=User.Types.STAFF
        )

    def _require_jwt_cookies(self, user) -> None:
        """Client will attach valid JWT Cookies"""
        access, refresh = get_tokens_for_user(user=user)
        self.client.cookies.load({
            'access': access,
            'refresh': refresh,
        })

    def test_obtain_jwt(self):
        response = self.client.post('/api/auth/token/', {
            'email': 'test@gmail.com',
            'password': 'testing123'
        })
        res_json = response.json()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('access', res_json)
        self.assertIn('refresh', res_json)

    def test_obtain_jwt_missing_fields(self):
        response = self.client.post('/api/auth/token/', {
            'email': 'test@gmail.com',
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['This field is required.']})

    def test_obtain_jwt_user_not_found(self):
        response = self.client.post('/api/auth/token/', {
            'email': 'nouser@gmail.com',
            'password': 'nouser123'
        })
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'No active account found with the given credentials'})

    def test_refresh_jwt_refresh_in_request(self):
        access, refresh = get_tokens_for_user(self.user)
        res_refresh_token = self.client.post('/api/auth/token/refresh/', data={
            'refresh': refresh
        })
        refresh_data = res_refresh_token.json()
        self.assertEqual(res_refresh_token.status_code, HTTP_200_OK)
        self.assertIn('access', refresh_data)
        self.assertNotEqual(access, refresh_data['access'])

    def test_refresh_jwt_refresh_in_cookie(self):
        self._require_jwt_cookies(self.user)
        prev_access = self.client.cookies['access']
        res_refresh_token = self.client.post('/api/auth/token/refresh/', data={})
        refresh_data = res_refresh_token.json()
        self.assertEqual(res_refresh_token.status_code, HTTP_200_OK)
        self.assertIn('access', refresh_data)
        self.assertNotEqual(prev_access, refresh_data['access'])

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

    def test_verify_jwt_token_in_request(self):
        access, refresh = get_tokens_for_user(self.user)
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

    def test_verify_jwt_token_in_cookie(self):
        self._require_jwt_cookies(user=self.user)
        response = self.client.post('/api/auth/token/verify/', {})
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_verify_jwt_no_token_in_data_nor_cookies(self):
        response = self.client.post('/api/auth/token/verify/', {})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'token': ['This field is required.']})

    def test_verify_jwt_token_invalid(self):
        response = self.client.post('/api/auth/token/verify/', {
            'token': 'totally_legit_jwt_xd'
        })
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Token is invalid or expired', 'code': 'token_not_valid'})

    def test_verify_jwt_invalid_token_in_cookie(self):
        self.client.cookies.load({
            'access': 'blablabla'
        })
        response = self.client.post('/api/auth/token/verify/', {})
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Token is invalid or expired', 'code': 'token_not_valid'})

    def test_logout(self):
        self._require_jwt_cookies(user=self.user)
        self.assertEqual(BlacklistedToken.objects.all().count(), 0)
        response = self.client.get('/api/auth/logout/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(BlacklistedToken.objects.all().count(), 1)
        self.assertEqual(response.json(), {'message': 'Logout successful!'})

    def test_logout_cookies_not_found(self):
        response = self.client.get('/api/auth/logout/')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(),
            {'message': "Could not logout! Cookie 'refresh' not found in request!"}
        )

    def test_get_current_user(self):
        self._require_jwt_cookies(user=self.user)
        response = self.client.get('/api/users/me/', {})
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json(), UserSerializer(self.user).data)

    def test_get_current_user_without_cookies_and_headers(self):
        response = self.client.get('/api/users/me/', {})
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_get_current_user_invalid_token(self):
        self.client.cookies.load({
            'access': 'qwerty1234567890'
        })
        response = self.client.get('/api/users/me/', {})
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(),
            {
                'detail': 'Given token not valid for any token type',
                'code': 'token_not_valid',
                'messages': [
                    {
                        'token_class': 'AccessToken',
                        'token_type': 'access',
                        'message': 'Token is invalid or expired'
                    }
                ]
            }
        )

    def test_create_doctor(self):
        response = self.client.post('/api/users/', {
            'email': 'test@gmail5.com',
            'password': 'testing1234',
            'first_name': 'abc',
            'last_name': 'abc',
            'birth_date': '2020-10-11',
            'type': User.Types.DOCTOR,
        })
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        user = User.objects.get(email="test@gmail5.com")
        self.assertEqual(response.json(), RegisterUserSerializer(user).data)

    def test_create_patient(self):
        response = self.client.post('/api/users/', {
            'email': 'test@gmail1.com',
            'password': 'testing1234',
            'first_name': 'abc',
            'last_name': 'abc',
            'birth_date': '2020-10-11',
            'type': User.Types.PATIENT,
        })
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        user = User.objects.get(email="test@gmail1.com")
        self.assertEqual(response.json(), RegisterUserSerializer(user).data)

    def test_create_user_empty(self):
        response = self.client.post('/api/users/', {
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_check_if_registered_doctor_active(self):
        response = self.client.post('/api/users/', {
            'email': 'test@gmail1234.com',
            'first_name': 'abc',
            'last_name': 'abc',
            'password': 'testing1234',
            'birth_date': '2020-10-11',
            'type': User.Types.DOCTOR,
        })
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        user = User.objects.get(email="test@gmail1234.com")
        self.assertEqual(response.json(), UserSerializer(user).data)
        self.assertEqual(user.is_active, False)

    def test_create_doctor_with_wrong_birth_date(self):
        response = self.client.post('/api/users/', {
            'email': 'test@gmail1234.com',
            'first_name': 'abc',
            'last_name': 'abc',
            'password': 'testing1234',
            'birth_date': timezone.now().date() + timedelta(days=2),
            'type': User.Types.DOCTOR,
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'birth_date': ['Invalid date! Birth date cannot be in the future.']})

    def test_create_user_without_email(self):
        response = self.client.post('/api/users/', {
            'first_name': 'abc',
            'last_name': 'abc',
            'password': 'testing1234',
            'birth_date': '2020-10-11',
            'type': User.Types.DOCTOR,
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'email': ['This field is required.']})

    def test_create_user_without_first_name(self):
        response = self.client.post('/api/users/', {
            'email': 'niceemail@gmail.com',
            'last_name': 'abc',
            'password': 'testing1234',
            'birth_date': '2020-10-11',
            'type': User.Types.DOCTOR,
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'first_name': ['This field is required.']})

    def test_create_user_without_last_name(self):
        response = self.client.post('/api/users/', {
            'email': 'niceemail@gmail.com',
            'first_name': 'abc',
            'password': 'testing1234',
            'birth_date': '2020-10-11',
            'type': User.Types.DOCTOR,
        })
        self.assertEqual(response.json(), {'last_name': ['This field is required.']})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_create_user_without_birth_date(self):
        response = self.client.post('/api/users/', {
            'email': 'test23@gmail.com',
            'first_name': 'abc',
            'last_name': 'abc',
            'password': 'testing1234',
            'type': User.Types.DOCTOR,
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'birth_date': ['This field is required.']})

    def test_create_user_without_type(self):
        response = self.client.post('/api/users/', {
            'email': 'test88@gmail.com',
            'first_name': 'abc',
            'last_name': 'abc',
            'password': 'testing1234',
            'birth_date': '2020-10-11',
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'type': ['This field is required.']})

    def test_create_user_without_password(self):
        response = self.client.post('/api/users/', {
            'email': 'testtttt@gmail.com',
            'first_name': 'abc',
            'last_name': 'abc',
            'birth_date': '2020-10-11',
            'type': User.Types.DOCTOR,
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password': ['This field is required.']})

    def test_list_users(self):
        self._require_jwt_cookies(self.user)

        response = self.client.post('/api/users/', {
            'email': 'test@gmail6.com',
            'password': 'testing1234',
            'first_name': 'abc',
            'last_name': 'abc',
            'birth_date': '2020-10-11',
            'type': User.Types.PATIENT,
        })
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_list_current_users(self):
        self._require_jwt_cookies(self.user)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_deny_update_patch_user(self):
        response = self.client.post('/api/users/', {
            'email': 'test@gmail15.com',
            'password': 'testing1234',
            'first_name': 'abc',
            'last_name': 'abc',
            'birth_date': '2020-10-11',
            'type': User.Types.PATIENT,
        })
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        user = User.objects.get(email="test@gmail15.com")
        response = self.client.patch(f'/api/users/{user.id}/', {'first_name': 'bca'})
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_deny_update_put_user(self):
        response = self.client.post('/api/users/', {
            'email': 'test@gmail15.com',
            'password': 'testing1234',
            'first_name': 'abc',
            'last_name': 'abc',
            'birth_date': '2020-10-11',
            'type': User.Types.PATIENT,
        })
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        user = User.objects.get(email="test@gmail15.com")
        response = self.client.put(f'/api/users/{user.id}/', {'first_name': 'bca'})
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_deny_delete_user(self):
        response = self.client.post('/api/users/', {
            'email': 'test@gmail15.com',
            'password': 'testing1234',
            'first_name': 'abc',
            'last_name': 'abc',
            'birth_date': '2020-10-11',
            'type': User.Types.PATIENT,
        })
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        user = User.objects.get(email="test@gmail15.com")
        response = self.client.delete(f'/api/users/{user.id}/')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_users_doctor_filter(self):
        self._require_jwt_cookies(user=self.user)
        User.objects.create_user(
            email="test11@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.DOCTOR
        )
        User.objects.create_user(
            email="test21@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.DOCTOR
        )
        User.objects.create_user(
            email="test31@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.PATIENT
        )
        User.objects.create_user(
            email="test41@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.PATIENT
        )
        response = self.client.get('/api/users/?type=DOCTOR')
        self.assertEqual(response.status_code, HTTP_200_OK)
        result = User.objects.filter(type='DOCTOR')
        self.assertEqual(response.json()['results'], UserSerializer(result, many=True).data)

    def test_users_patient_filter(self):
        self._require_jwt_cookies(user=self.user)
        User.objects.create_user(
            email="test12@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.DOCTOR
        )
        User.objects.create_user(
            email="test22@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.DOCTOR
        )
        User.objects.create_user(
            email="test32@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.PATIENT
        )
        User.objects.create_user(
            email="test42@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.PATIENT
        )
        response = self.client.get('/api/users/?type=PATIENT')
        self.assertEqual(response.status_code, HTTP_200_OK)
        result = User.objects.filter(type='PATIENT')
        self.assertEqual(response.json()['results'], UserSerializer(result, many=True).data)

    def test_users_bad_filter(self):
        self._require_jwt_cookies(user=self.user)
        User.objects.create_user(
            email="test13@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.DOCTOR
        )
        User.objects.create_user(
            email="test23@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.DOCTOR
        )
        User.objects.create_user(
            email="test33@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.PATIENT
        )
        User.objects.create_user(
            email="test45@gmail.com", password="test1",
            first_name="", last_name="", type=User.Types.PATIENT
        )
        response = self.client.get('/api/users/?type=APPLE')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'type': ['Select a valid choice. APPLE is not one of the available choices.']}
        )
