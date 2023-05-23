from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    class Gender(models.IntegerChoices):
        male = 1
        female = 2
        other = 3

    created_at = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
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

    follows = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="followed_by",
        symmetrical=False,
        blank=True,
    )

    def __str__(self):
        return self.full_name
