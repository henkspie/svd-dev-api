"""
Tests for models
"""
import datetime as dt
from django.test import TestCase
from django.contrib.auth import get_user_model
# from django.test import Client

from core.models import Member
from famTree.models import Event

test_members = [
    {
        "firstname": "Jan Karel",
        "lastname": "User",
        "birthday": dt.date(1958, 1, 6),
    },
    {
        "firstname": "None",
        "lastname": "Tester",
        "birthday": dt.date(1950, 1, 6),
    }
]


class model_tests(TestCase):
    """ Test models"""
    # def setUp(self):
    #     user = Client().force_login(user="Henk_19500106")

    #     print(f"User: {user}")
    #     for fn, name, bd in test_members:
    #         print(bd)
    #         member = Member.objects.create(
    #         firstname=fn,
    #         lastname=name,
    #         birthday=bd,
    #         editor=user
    #         )

    def test_create_svdUser_with_username_successful(self):
        """ Test creating a SvdUser with an username is successful."""
        username = 'Tester_19500106'
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
        for user, expected in sample_svdUsers:
            users = get_user_model().objects.create_user(svdUser=user, password="testpass123")
            self.assertEqual(users.svdUser, expected)

    def test_wrong_format_new_user_raises_error(self):
        """Test wrong format raises error. """
        wrong_users = [
            "User_1950106",
            "User_195001060",
            "User_18500106",
        ]
        for user in wrong_users:
            with self.assertRaisesRegex(NameError, "Not a correct svdUser name given."):
                get_user_model().objects.create_user(svdUser=user, password="testpass123")

    def test_create_simple_superuser(self):
        """ Test creating a superuser with svdUser constructed"""
        user = get_user_model().objects.create_superuser(
            svdUser="user_19500106",
            password="testpass123",
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.svdUser, "User_19500106")

    def test_create_user_with_name_and_birthday(self):
        """ Test create a user with name and birthday"""
        user = get_user_model().objects.create_user(
            # test = True,
            name="Tester",
            birthday="1976-01-14",
            password="testpass123",
            email="Tester@example.com"
        )

        self.assertEqual(user.svdUser, "Tester_19760114")
        self.assertTrue(user.check_password("testpass123"))

    def test_adding_member_in_familyTree(self):
        """Test adding a member to the family tree is successful."""
        user = get_user_model().objects.create_user(
            svdUser='User_19500106',
            password="testpass123",
        )

        name = "User"
        member = Member.objects.create(
            firstname="Jan Karel",
            lastname=name,
            birthday="1958-01-06",
            editor=user)

        self.assertEqual(member.lastname, name)
        self.assertEqual(member.editor, user)

    def test_svdUser_is_in_member_db(self):
        user = get_user_model().objects.create_user(
            svdUser='User_19500106',
            password="testpass123",
        )
        for kwargs in test_members:
            kwargs['editor'] = user
            # print(kwargs)
            Member.objects.create(**kwargs)
            # print(x)
        pass

    def test_create_event(self):
        user = get_user_model().objects.create_user(
            svdUser='User_19500106',
            password="testpass123",
        )
        event = Event.objects.create(
            event_type="birth",
            date=dt.date(1967, 8, 9),
            editor=user,
        )

        self.assertEqual(str(event), event.event_type)
