from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from profiles.models import Profile
from profiles.serializers import ProfileSerializer

PROFILE_URL = reverse("profiles:profile-list")


class UnauthenticatedProfileApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(PROFILE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedProfileApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@mail.com",
            password="test_password",
        )

        self.client.force_authenticate(self.user)

    def test_list_profiles(self):
        Profile.objects.create(
            user=self.user,
            first_name="Sample first_name",
            last_name="Sample last_name",
            gender=1,
            birth_date="2023-05-31",
            phone="1111111111",
        )

        user1 = get_user_model().objects.create_user(
            email="test_user1@mail.com",
            password="test_password1",
        )

        Profile.objects.create(
            user=user1,
            first_name="Sample first_name 1",
            last_name="Sample last_name 1",
            gender=2,
            birth_date="2022-05-31",
            phone="2222222222",
        )

        response = self.client.get(PROFILE_URL)
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_profile(self):
        payload = {
            "first_name": "Sample first_name 1",
            "last_name": "Sample last_name 1",
            "gender": 2,
            "birth_date": "2022-05-31",
            "phone": "2222222222",
        }

        response = self.client.post(PROFILE_URL + "create/", payload)
        profile = Profile.objects.get(id=response.data["id"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            if key == "birth_date":
                self.assertEqual(
                    payload[key], getattr(profile, key).strftime("%Y-%m-%d")
                )
            else:
                self.assertEqual(payload[key], getattr(profile, key))


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(
            email="test_user@mail.com",
            password="test_password",
        )
        Profile.objects.create(
            user=user,
            first_name="Sample first_name",
            last_name="Sample last_name",
            gender=1,
            birth_date="2023-05-31",
            phone="1111111111",
        )

    def test_created_at_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field("created_at").verbose_name
        self.assertEqual(field_label, "created at")

    def test_user_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field("user").verbose_name
        self.assertEqual(field_label, "user")

    def test_first_name_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_last_name_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field("last_name").verbose_name
        self.assertEqual(field_label, "last name")

    def test_gender_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field("gender").verbose_name
        self.assertEqual(field_label, "gender")

    def test_birth_date_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field("birth_date").verbose_name
        self.assertEqual(field_label, "birth date")

    def test_phone_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field("phone").verbose_name
        self.assertEqual(field_label, "phone")

    def test_image_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field("image").verbose_name
        self.assertEqual(field_label, "image")

    def test_follows_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field("follows").verbose_name
        self.assertEqual(field_label, "follows")

    def test_first_name_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 255)

    def test_last_name_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 255)

    def test_profile_str(self):
        profile = Profile.objects.get(id=1)
        expected_object_name = f"{profile.first_name} {profile.last_name}"
        self.assertEqual(str(profile), expected_object_name)

    def test_profile_full_name(self):
        profile = Profile.objects.get(id=1)
        expected_full_name = profile.full_name
        self.assertEqual(
            expected_full_name, f"{profile.first_name} {profile.last_name}"
        )
