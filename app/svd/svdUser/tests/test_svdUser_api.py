"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('svdUser:create')


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
            'email': 'test@example.com',
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
            'email': 'test@example.com',
            'name': "Tester",
            'birthday': "1976-01-14",
            'password': 'testpass123',
        }
        create_svdUser(**payload)
        # res = self.client.post(CREATE_USER_URL, payload)
        # print(res)
        # self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        with self.assertRaisesRegex(ValueError,"Save Error" ):
            self.client.post(CREATE_USER_URL, payload)

    def test_password_too_short_error(self):
        """ Test an error is returned if password is too short."""
        payload = {
            'email': 'test@example.com',
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
