"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class model_tests(TestCase):
    """ Test models"""

    def test_create_svdUser_with_username_successful(self):
        """ Test creating a SvdUser with an username is successful."""
        username = 'User_19500106'
        password = "testpass123"
        user = get_user_model().objects.create_user(
            svdUser=username,
            password=password,
        )

        self.assertEqual(user.svdUser, username)
        self.assertTrue(user.check_password(password))
