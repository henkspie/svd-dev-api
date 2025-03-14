"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('svdUser:create')
TOKEN_URL = reverse('svdUser:token')
ME_URL = reverse('svdUser:me')


def create_svdUser(**params):
    """ Create and return a new svdUser"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ Test the public features of the svdUser API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_svdUer_success(self):
        """ Test creating a svdUser is successful"""
        payload = {
            'email': 'test@exxxample.com',
            'password': 'testpass123',
            'name': 'Tester',
            'birthday': '1976-01-14',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        svdUser = get_user_model().objects.get(svdUser='Tester_19760114')
        self.assertTrue(svdUser.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_svdUser_is_unique(self):
        """  Test error returned if svdUser exists."""
        payload = {
            'email': 'test@exxxample.com',
            'name': "Tester",
            'birthday': "1976-01-14",
            'password': 'testpass123',
        }
        create_svdUser(**payload)
        # res = self.client.post(CREATE_USER_URL, payload)
        # print(res)
        # self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        with self.assertRaisesRegex(ValueError, "Save New User Error"):
            self.client.post(CREATE_USER_URL, payload)

    def test_password_too_short_error(self):
        """ Test an error is returned if password is too short."""
        payload = {
            'email': 'test@exxxample.com',
            'name': 'Tester',
            'birthday': '1976-01-14',
            'password': 'tes123',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            svdUser="Tester_19760114"
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ Test generates token for valid credentials"""
        svdUser_details = {
            'name': 'Tester',
            'birthday': '1976-01-14',
            'email': 'tester@exxxample.com',
            'password': 'testpass123',
        }
        create_svdUser(**svdUser_details)

        payload = {
            'svdUser': 'Tester_19760114',
            'password': 'testpass123',
        }
        res = self.client.post(TOKEN_URL, payload)
        # print(res)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """ Test return error for invalid credentials (wrong password)"""
        credentials = {
            'name': 'Tester',
            'birthday': '1976-01-14',
            'email': 'tester@exxxample.com',
            'password': 'goodpass123',
        }
        create_svdUser(**credentials)

        payload = {
            'svdUser': 'Tester_19760114',
            'password': 'badpass123',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """ Test return error for posting no password."""
        credentials = {
            'name': 'Tester',
            'birthday': '1976-01-14',
            'email': 'tester@exxxample.com',
            'password': 'goodpass123',
        }
        create_svdUser(**credentials)

        payload = {
            'svdUser': 'Tester_19760114',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """ Test authentication is required for user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """ Test API requests that require authentication."""

    def setUp(self):
        self.user = create_svdUser(
            name='Tester',
            birthday='1976-01-14',
            email='tester@exxxample.com',
            password='testpass123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """ Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'svdUser': 'Tester_19760114',
            'name': '',
            'birthday': None,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """ Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ Test updating the user profile for the authenticated user"""
        payload = {
            'name': 'User',
            'password': 'newpassword123',
        }
        res = self.client.patch(ME_URL, payload)
        # print(res.data)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
