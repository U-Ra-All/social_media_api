import os
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


def profile_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.first_name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/profiles/", filename)


class Profile(models.Model):
    class Gender(models.IntegerChoices):
        male = 1
        female = 2
        other = 3

    created_at = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    gender = models.PositiveSmallIntegerField(
        choices=Gender.choices, default=Gender.male
    )

    birth_date = models.DateField(null=True, blank=True, default=None)
    phone = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(
        null=True, blank=True, upload_to=profile_image_file_path
    )

    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True,
    )

    def __str__(self):
        return self.full_name
