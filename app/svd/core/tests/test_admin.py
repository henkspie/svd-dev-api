"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

from core.models import Member

from famTree.serializers import MemberSerializer

MEMBERS_URL = reverse("famTree:member-list")

class AdminSiteTests(TestCase):
    """ Django admin tests."""

    def setUp(self):
        """ Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            svdUser="Admin_19500106",
        )
        self.admin_user.set_password("testpass123")
        self.admin_user.save()
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            svdUser="User_19600106",
            email="user@example.com"
        )
        self.user.set_password("testpass123")
        self.user.save()

    def test_users_list(self):
        """ Test that users are listed on page."""
        url = reverse("admin:core_svduser_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.svdUser)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """ Test the edit svdUser page works."""
        url = reverse("admin:core_svduser_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ Test the create svdUser page works."""
        url = reverse("admin:core_svduser_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_admin_login_username(self):
        """ Test successful login"""
        # Define the login url
        url = reverse('admin:login')
        res = self.client.get(url)

        # A successful login returns 302 otherwise 200
        self.assertEqual(res.status_code, 302)

    def test_user_is_members(self):
        """ Test that the user is in the members db"""
        # def setUp(self):
        fixtures = ["fix_test_members.json"]
        pass

        # res = self.client.get(MEMBERS_URL)

        # members = Member.objects.all()
        # serializer = MemberSerializer(members, many=True)
        # print(f"{res.data} / {serializer.data}")
        # self.assertEqual(res.status_code, 200)
        # self.assertCountEqual(res.data, serializer.data)

