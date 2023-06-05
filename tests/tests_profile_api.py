from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from profiles.serializers import ProfileSerializer
from profiles.models import Profile

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
