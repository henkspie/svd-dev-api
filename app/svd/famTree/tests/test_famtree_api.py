""" Tests for famTree API."""
import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Member

from famTree.serializers import MemberSerializer, MemberDetailSerializer

MEMBERS_URL = reverse("famTree:member-list")


def detail_url(member_id):
    """ Create and return a member URL."""
    return reverse("famTree:member-detail", args=[member_id])


def create_member(user, **params):
    """ Create and return a member."""
    defaults = {
        "lastname": "Tester",
        "firstname": "Henricus",
        "call_name": "Henk",
        "sex": "M",
        "birthday": "1957-01-06",
        "birthday_txt": "1957",
        # "editor": user,
    }
    defaults.update(params)

    return Member.objects.create(editor=user, **defaults)


class PublicMemberAPITests(TestCase):
    """ Test unauthorized API request"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test authentication is required to call API."""
        res = self.client.get(MEMBERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMemberAPITest(TestCase):
    """ Test authenticated API request"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            svdUser="User_19760114",
            password="testpass123",
        )
        self.client.force_authenticate(self.user)
        # fixtures = ['fixtures/test_members.json']

    def test_retrieve_members(self):
        """ Test retrieving a list of members."""
        create_member(user=self.user)
        Member.objects.create(
            lastname="Tester",
            firstname="Frea",
            call_name="Free",
            sex="F",
            birthday="1951-02-18",
            birthday_txt="",
            editor=self.user)
        Member.objects.create(
            lastname="Tester",
            firstname="Johannes",
            call_name="Jan",
            sex="M",
            birthday="1916-09-23",
            birthday_txt="",
            editor=self.user)

        res = self.client.get(MEMBERS_URL)

        members = Member.objects.all()          # .order_by("birthday")
        serializer = MemberSerializer(members, many=True)
        # print(f"{res.data} / {serializer.data}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertListEqual(res.data, serializer.data)

    def test_get_member_detail(self):
        """ Test get member detail."""
        member = create_member(user=self.user)

        url = detail_url(member.id)
        res = self.client.get(url)

        serializer = MemberDetailSerializer(member)
        # print(f"{res.data} / {serializer.data}")
        self.assertEqual(res.data, serializer.data)

    def test_create_member(self):
        """ Test creating a member with the API."""
        payload = {
        "lastname": "Tester",
        "firstname": "Henricus",
        "call_name": "Henk",
        "sex": "M",
        "birthday": datetime.date(1957, 1, 6),
        "birthday_txt": "1957",
        }
        res = self.client.post(MEMBERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        member = Member.objects.get(id=res.data['id'])
        for key, value in payload.items():
            self.assertEqual(getattr(member, key), value)
        self.assertEqual(member.editor, self.user)