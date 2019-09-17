"""Registration tests"""

# Standard Library
from unittest.mock import patch

# Models
from ...users.models import User, Profile

# Django REST Framework
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

# Tasks
from ...taskapp.tasks import gen_verification_token

USER_DATA = {
    'first_name': 'Test',
    'last_name': 'User',
    'email': 'test@user.com',
    'username': 'test_user',
    'password': 'Testpassword123',
}
CELERY_SEND_EMAIL = 'prm.users.serializers.send_confirmation_email.delay'


def create_user(**kwargs):
    return User.objects.create_user(**kwargs)


class PublicUserViewsTestCase(APITestCase):
    """ Test public api endpoints and token validation, generation"""

    def setUp(self):
        self.urls = {
            'signup': '/users/signup/',
            'verify': '/users/verify/',
            'login': '/users/login/',
            'profile': '/users/profile/'
        }
        return super().setUp()

    def test_signup_doesnt_accept_get(self):
        """Verify request succeed"""
        response = self.client.get(self.urls['signup'])
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_user_signup_require_fields(self):
        """Cannot send empty request to signup"""
        response = self.client.post(self.urls['signup'], None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch(CELERY_SEND_EMAIL)
    def test_create_valid_user_success(self, send_email_mock):
        """Creating an user with valid credentials creates the user, a
        profile and sets is_active to false"""

        payload = USER_DATA.copy()
        payload['password_confirmation'] = payload['password']
        response = self.client.post(self.urls['signup'], data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        send_email_mock.assert_called_once()
        self.assertEqual(User.objects.count(), 1)

        self.assertIn('profile', response.data)
        response.data.pop('profile')
        user = User.objects.get(**response.data)
        self.assertTrue(Profile.objects.filter(user=user).exists())

        self.assertEqual(user.username, USER_DATA['username'])
        self.assertTrue(user.check_password(USER_DATA['password']))
        self.assertFalse(user.is_active)

    @patch(CELERY_SEND_EMAIL)
    def test_user_already_exists(self, _):
        """Creating an user with the same email or password fails"""
        create_user(**USER_DATA)

        payload = USER_DATA.copy()
        payload['email'] = 'another@email.com'
        payload['password_confirmation'] = payload['password']

        # Check for same username
        response = self.client.post(self.urls['signup'], data=payload)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

        # Check for same email
        payload['email'] = USER_DATA['email']
        payload['username'] = 'another_user'

        response = self.client.post(self.urls['signup'], data=payload)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    @patch(CELERY_SEND_EMAIL)
    def test_password_too_short(self, _):
        """Users cannot register with an easy-to-guess passwrod"""
        payload = USER_DATA.copy()
        payload['password'] = payload['password_confirmation'] = \
            'password123'

        response = self.client.post(self.urls['signup'], data=payload)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    @patch(CELERY_SEND_EMAIL)
    def test_unverified_user_cannot_login(self, _):
        """Until the user verifies with the issued token, he won't be able
        to log in"""
        payload = USER_DATA.copy()
        payload['password_confirmation'] = payload['password']

        response = self.client.post(self.urls['signup'], data=payload)
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)
        response.data.pop('profile')

        login_data = {
            'username': USER_DATA['username'],
            'password': USER_DATA['password']
        }

        response = self.client.post(self.urls['login'], data=login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch(CELERY_SEND_EMAIL)
    def test_verify_token_activates_user(self, _):
        """After generating the token, it must be validated on the
        verify view"""
        payload = USER_DATA.copy()
        payload['password_confirmation'] = payload['password']

        response = self.client.post(self.urls['signup'], data=payload)
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)
        response.data.pop('profile')
        user = User.objects.get(**response.data)
        self.assertFalse(user.is_active)
        token = gen_verification_token(user)

        token_res = self.client.post(f"{self.urls['verify']}?token={token}")
        self.assertTrue(token_res.status_code, status.HTTP_200_OK)
        user = User.objects.get(**response.data)
        self.assertTrue(user.is_active)

    @patch(CELERY_SEND_EMAIL)
    def test_verified_user_can_login(self, _):
        """After verification user can login normally and get a token"""
        payload = USER_DATA.copy()
        payload['password_confirmation'] = payload['password']
        response = self.client.post(self.urls['signup'], data=payload)
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)
        response.data.pop('profile')

        user = User.objects.get(**response.data)
        token = gen_verification_token(user)
        token_res = self.client.post(f"{self.urls['verify']}?token={token}")
        self.assertTrue(token_res.status_code, status.HTTP_200_OK)
        login_data = {
            'email': USER_DATA['email'],
            'password': USER_DATA['password']
        }

        login_res = self.client.post(self.urls['login'], login_data)
        self.assertTrue(login_res.status_code, status.HTTP_200_OK)
        self.assertIn('token', login_res.data)
        self.assertEqual(Token.objects.count(), 1)

    def test_only_authorized_user_can_check_profile(self):
        user = create_user(**USER_DATA)
        user.is_active = True
        user.save()
        Profile.objects.create(user=user)

        response = self.client.get(self.urls['profile'])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
