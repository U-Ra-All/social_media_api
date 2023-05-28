# Generated by Django 4.2.1 on 2023-05-28 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0003_alter_profile_image"),
        ("posts", "0005_like"),
    ]

    operations = [
        migrations.AddField(
            model_name="like",
            name="user_profile",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to="profiles.profile",
            ),
        ),
    ]
