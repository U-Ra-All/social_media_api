# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
#
# from posts.models import Post
# from posts.serializers import PostSerializer
# from profiles.models import Profile
#
# POST_URL = reverse("posts:post-list")
#
#
# def sample_post(**params):
#     user_profile = sample_profile()
#
#     defaults = {
#         "title": "Sample title",
#         "body": "Sample body",
#         "user_profile": user_profile,
#     }
#     defaults.update(params)
#
#     return Post.objects.create(**defaults)
#
#
# def sample_profile(**params):
#     user = sample_user()
#     defaults = {
#         "user": user,
#         "first_name": "Sample first_name",
#         "last_name": "Sample last_name",
#         "gender": 1,
#         "birth_date": "2023-05-31",
#         "phone": "1111111111",
#     }
#     defaults.update(params)
#
#     return Profile.objects.create(**defaults)
#
#
# def sample_user():
#
#     return get_user_model().objects.create_user(
#         "test@mail.com",
#         "test_password",
#     )
#
#
# class UnauthenticatedPostApiTest(TestCase):
#     def setUp(self) -> None:
#         self.client = APIClient()
#
#     def test_auth_required(self):
#         response = self.client.get(POST_URL)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class AuthenticatedPostApiTest(TestCase):
#     def setUp(self) -> None:
#         self.client = APIClient()
#         self.user = sample_user()
#         self.client.force_authenticate(self.user)
#
#     def test_list_posts(self):
#         sample_post()
#         sample_post(
#             title="Sample title 1",
#             body="Sample body 1",
#             user_profile=sample_profile(user=self.user),
#         )
#         sample_post(
#             title="Sample title 2",
#             body="Sample body 2",
#             user_profile=sample_profile(user=self.user),
#         )
#
#         response = self.client.get(POST_URL)
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, serializer.data)
#
#     def test_create_post_forbidden(self):
#         payload = {
#             "first_name": "Sample first name",
#             "last_name": "Sample last name",
#         }
#
#         response = self.client.post(POST_URL, payload)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#
# class AdminPostApiTest(TestCase):
#     def setUp(self) -> None:
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             "test@test.com",
#             "test_password",
#             is_staff=True
#         )
#         self.client.force_authenticate(self.user)
#
#     def test_create_post(self):
#         payload = {
#             "first_name": "Sample first name",
#             "last_name": "Sample last name",
#         }
#
#         response = self.client.post(POST_URL, payload)
#         post = Post.objects.get(id=response.data["id"])
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         for key in payload:
#             self.assertEqual(payload[key], getattr(post, key))
#
#
# class PostModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         sample_post()
#
#     def test_first_name_label(self):
#         post = Post.objects.get(id=1)
#         field_label = post._meta.get_field("first_name").verbose_name
#         self.assertEqual(field_label, "first name")
#
#     def test_last_name_label(self):
#         post = Post.objects.get(id=1)
#         field_label = post._meta.get_field("last_name").verbose_name
#         self.assertEqual(field_label, "last name")
#
#     def test_first_name_max_length(self):
#         post = Post.objects.get(id=1)
#         max_length = post._meta.get_field("first_name").max_length
#         self.assertEqual(max_length, 255)
#
#     def test_last_name_max_length(self):
#         post = Post.objects.get(id=1)
#         max_length = post._meta.get_field("last_name").max_length
#         self.assertEqual(max_length, 255)
#
#     def test_post_str(self):
#         post = Post.objects.get(id=1)
#         expected_object_name = f"{post.first_name} {post.last_name}"
#         self.assertEqual(str(post), expected_object_name)
#
#     def test_post_full_name(self):
#         post = Post.objects.get(id=1)
#         expected_full_name = post.full_name
#         self.assertEqual(expected_full_name, f"{post.first_name} {post.last_name}")
