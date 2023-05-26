# Generated by Django 4.2.1 on 2023-05-26 08:34

from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                (
                    "gender",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Male"), (2, "Female"), (3, "Other")], default=1
                    ),
                ),
                ("birth_date", models.DateField(blank=True, default=None, null=True)),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "image",
                    models.ImageField(
                        null=True, upload_to=profiles.models.profile_image_file_path
                    ),
                ),
                (
                    "follows",
                    models.ManyToManyField(
                        blank=True, related_name="followed_by", to="profiles.profile"
                    ),
                ),
            ],
        ),
    ]
