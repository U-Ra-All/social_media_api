import os
import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
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
        Profile, on_delete=models.CASCADE, related_name="post", default=1
    )

    def __str__(self):
        return self.title
