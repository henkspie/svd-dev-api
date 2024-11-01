"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """ Django admin tests."""

    def setUp(self):
        """ Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            svdUser="Admin_19500106",
            password="testpass123"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            svdUser="User_19600106",
            password="testpass123",
            email="user@example.com"
        )

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

        res = self.client.post('url',
            svdUser=self.user.svdUser,
            password="testpass123",
            email="user@example.com",
            follow=True,
        )
        print(res)
        # A successful login returns 302 otherwise 200
        self.assertTrue(res.context['svdUser'].is_authenticated)
        self.assertEqual(res.status_code, 302)
        self.assertContains(res, self.user.svdUser)