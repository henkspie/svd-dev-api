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

    def test_new_user_svdUser_normalized(self):
        """ Test the svdUser is normalized for new user."""

        sample_svdUsers = [
             ["User_19500601", "User_19500601"],
             ["UsEr_19500602", "User_19500602"],
             ["User-Peter_19500601", "User-peter_19500601"],
             ["USEr-peter_19500602", "User-peter_19500602"],
        ]
        for svdUser, expected in sample_svdUsers:
            user = get_user_model().objects.create_user(svdUser, "testpass123")
            self.assertEqual(user.svdUser, expected)

    def test_wrong_format_new_user_raises_error(self):
        """Test wrong format raises error. """
        wrong_users = [
            "User_1950106",
            "User_195010106",
            "User_18500106",
        ]
        for svdUser in wrong_users:
            with self.assertRaises(ValueError):
                get_user_model().objects.create_user(svdUser, "testpass123")

    def test_create_superuser(self):
        """ Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            "user_19500106",
            "testpass123",
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.svdUser, "User_19500106")

    # def test_svdUser_is_in_familyTree(self):
    #     """Test the svUser is a member of the family tree."""
    #     firstname = "Jan Karel"
    #     name = "User"
    #     birthday = "1959-01-06"
    #     member = FamilyTree.objects.create(firstname=firstname,
    #                                        name=name, birthday=birthday)

    #     username = "User_19500106"
