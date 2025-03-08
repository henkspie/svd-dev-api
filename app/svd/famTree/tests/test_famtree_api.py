""" Tests for famTree API."""

import datetime
import os
import tempfile

from PIL import Image

from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core import models
from core.models import Member

from famTree.serializers import MemberSerializer, MemberDetailSerializer

MEMBERS_URL = reverse("famTree:member-list")
DAD_MIN_YEARS = datetime.timedelta(days=17*365)
DAD_MAX_YEARS = datetime.timedelta(days=62*365)
MAM_MIN_YEARS = datetime.timedelta(days=15*365)
MAM_MAX_YEARS = datetime.timedelta(days=49*365)
CREATE_USER_URL = reverse('svdUser:create')


def detail_url(member_id):
    """ Create and return a member URL."""
    return reverse("famTree:member-detail", args=[member_id])


def image_upload_url(member_id):
    """ Create and return an image URL"""
    return reverse("famTree:member-upload-image", args=[member_id])


def create_member(user, **params):
    """ Create and return a member."""
    defaults = {
        "lastname": "Tester",
        "firstname": "Henricus",
        "call_name": "Henk",
        "sex": "M",
        "birthday": datetime.date(1957, 1, 6),
        "birthday_txt": "1957",
    }
    defaults.update(params)

    return Member.objects.create(editor=user, **defaults)


def create_user(**params):
    """ Create and return a new user"""
    return get_user_model().objects.create_user(**params)


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
        self.user = create_user(
            svdUser="Tester_19760114",
            password="testpass123",
        )
        self.client.force_authenticate(self.user)

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

        members = Member.objects.all()        # .order_by("id")
        serializer = MemberSerializer(members, many=True)
        # print(f"{res.data} / // / {members}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertCountEqual(res.data, serializer.data)

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

    def test_partial_update(self):
        """ Test partial update of a member"""
        original_data = {"lastname": "Tester", "call_name": "Henk"}
        member = create_member(
            user=self.user,
            lastname=original_data["lastname"],
            firstname="Hendricus",
            call_name=original_data["call_name"],
            sex="M",
            birthday=datetime.date(1957, 1, 6),
            birthday_txt="1957",
        )

        change_name = {"firstname": "Henricus"}
        url = detail_url(member.id)
        res = self.client.patch(url, change_name)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        member.refresh_from_db()
        self.assertEqual(member.lastname, original_data["lastname"])
        self.assertEqual(member.call_name, original_data["call_name"])
        self.assertEqual(member.firstname, change_name["firstname"])
        self.assertEqual(member.editor, self.user)

    def test_full_update(self):
        """ Test full update of member."""
        member = create_member(self.user)

        payload = {
            "lastname": "User",
            "firstname": "Johannes",
            "call_name": "Jan",
            "sex": "M",
            "birthday": datetime.date(1917, 11, 26),
            "birthday_txt": "1917",
        }
        url = detail_url(member.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        member.refresh_from_db()
        for key, value in payload.items():
            self.assertEqual(getattr(member, key), value)
        self.assertEqual(member.editor, self.user)

    def test_update_user_returns_error(self):
        """ Test changing the member editor results in an error."""
        new_user = create_user(
            svdUser="User_19740214",
            password="newuserpass123",
        )
        member = create_member(user=self.user)

        payload = {"user": new_user.id}
        url = detail_url(member.id)
        self.client.patch(url, payload)

        member.refresh_from_db()
        self.assertEqual(member.editor, self.user)

    def test_delete_member(self):
        """ Test deleting a member successful."""
        member = create_member(user=self.user)

        url = detail_url(member.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Member.objects.filter(id=member.id).exists())

    def test_delete_other_users_members(self):
        """ Test trying to delete another users member."""
        new_user = create_user(
            svdUser="User_19700224",
            password="newuserpass123",
        )
        member = create_member(user=new_user)
        # print(self.user, new_user)
        url = detail_url(member.id)
        self.client.delete(url)
        # print(res)
        # self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Member.objects.filter(id=member.id).exists())

    def test_father_and_Mother_to_the_member(self):
        """ Test adding a father and a mother to the member."""
        member = create_member(user=self.user)
        mother = Member.objects.create(
            lastname="Tester",
            firstname="Frea",
            call_name="Free",
            sex="F",
            birthday=datetime.date(1951, 2, 18),
            birthday_txt="",
            editor=self.user)
        father = Member.objects.create(
            lastname="Tester",
            firstname="Johannes",
            call_name="Jan",
            sex="M",
            birthday=datetime.date(1916, 9, 23),
            birthday_txt="",
            editor=self.user)
        payload = {"father": father.id, "mother": mother.id}
        url = detail_url(member.id)
        self.client.patch(url, payload)

        member.refresh_from_db()
        self.assertEqual(member.mother.id, mother.id)
        self.assertEqual(member.father.lastname, father.lastname)
        # print(f"Verjaardagen: {member.birthday} {father.birthday}")
        self.assertLess(father.birthday+DAD_MIN_YEARS, member.birthday)
        self.assertLess(member.birthday, father.birthday+DAD_MAX_YEARS)

    @patch('core.models.uuid.uuid4')
    def test_member_file_image_uuid(self, mock_uuid):
        """ Test generating image path"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.member_image_filepath(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/members/{uuid}.jpg')


class FixTestMembers(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.get(id=1)  # user 1 is needed  to load fixtures
        self.client.force_authenticate(self.user)

    fixtures = ["fixtures/fix_test_members.json"]

    def test_members_are_loaded(self):
        """ Test members are loaded from fixtures"""
        members = Member.objects.all()
        self.assertEqual(len(members), 7)

        res = self.client.get(MEMBERS_URL)

        serializer = MemberSerializer(members, many=True)
        # print(f"{res.data} / // / {members}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertCountEqual(res.data, serializer.data)

    def test_user_is_in_members(self):
        """ Test create a user is in members"""
        payload = {
            'name': 'Tester',
            'birthday': '1951-02-18',
            'email': 'tester@testemail.com',
            'password': 'testpass123',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        svdUser = get_user_model().objects.get(svdUser='Tester_19510218')
        self.assertTrue(svdUser.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_is_not_in_members(self):
        """ Test failure create a user not in members"""
        payload = {
            'name': 'Tester',
            'birthday': '1951-02-17',
            'email': 'tester@testemail.com',
            'password': 'testpass123',
        }

        with self.assertRaisesRegex(ValueError, "You are not in the db"):
            self.client.post(CREATE_USER_URL, payload)


class ImageUploadTests(TestCase):
    """ Tests for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            svdUser="Tester_19500106",
            password='testpass123'
        )
        self.client.force_authenticate(self.user)
        self.member = create_member(user=self.user)

    def tearTown(self):
        self.member.image.delete()

    def test_upload_image(self):
        """ Test uploading an image to a member"""
        url = image_upload_url(self.member.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)
            payload = {"image": image_file}
            res = self.client.post(url, payload, format="multipart")

        self.member.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.member.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading invalid image."""
        url = image_upload_url(self.member.id)
        payload = {"image": "notanimage"}
        res = self.client.post(url, payload, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
