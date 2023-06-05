from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from posts.models import Post
from posts.serializers import PostSerializer
from profiles.models import Profile

POST_URL = reverse("posts:post-list")


class UnauthenticatedPostApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(POST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPostApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@mail.com",
            password="test_password",
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name="Sample first_name",
            last_name="Sample last_name",
            gender=1,
            birth_date="2023-05-31",
            phone="1111111111",
        )
        self.client.force_authenticate(self.user)

    def test_list_posts(self):
        Post.objects.create(
            title="Sample title 1",
            body="Sample body 1",
            user_profile=self.profile,
        )

        Post.objects.create(
            title="Sample title 2",
            body="Sample body 2",
            user_profile=self.profile,
        )

        response = self.client.get(POST_URL)
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("response.data: ", response.data)
        print("serializer.data: ", serializer.data)
        self.assertEqual(response.data, serializer.data)

    def test_create_post(self):
        payload = {
            "title": "Sample title",
            "body": "Sample body",
        }

        response = self.client.post(POST_URL + "create/", payload)
        post = Post.objects.get(id=response.data["id"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(post, key))
