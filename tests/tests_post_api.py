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


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(
            email="test_user@mail.com",
            password="test_password",
        )
        profile = Profile.objects.create(
            user=user,
            first_name="Sample first_name",
            last_name="Sample last_name",
            gender=1,
            birth_date="2023-05-31",
            phone="1111111111",
        )
        Post.objects.create(
            title="Sample title 1",
            body="Sample body 1",
            user_profile=profile,
        )

    def test_created_at_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field("created_at").verbose_name
        self.assertEqual(field_label, "created at")

    def test_title_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field("title").verbose_name
        self.assertEqual(field_label, "title")

    def test_body_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field("body").verbose_name
        self.assertEqual(field_label, "body")

    def test_image_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field("image").verbose_name
        self.assertEqual(field_label, "image")

    def test_user_profile_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field("user_profile").verbose_name
        self.assertEqual(field_label, "user profile")

    def test_title_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field("title").max_length
        self.assertEqual(max_length, 255)

    def test_post_str(self):
        post = Post.objects.get(id=1)
        expected_object_name = f"{post.title}"
        self.assertEqual(str(post), expected_object_name)
