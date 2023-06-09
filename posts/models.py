import os
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from profiles.models import Profile


def post_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/posts/", filename)


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    body = models.TextField()

    image = models.ImageField(
        null=True, blank=True, upload_to=post_image_file_path
    )

    user_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="posts"
    )

    def __str__(self):
        return self.title


class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes"
    )
    user_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="likes"
    )


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    user_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return self.body
