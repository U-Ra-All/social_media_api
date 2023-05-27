# Generated by Django 4.2.1 on 2023-05-27 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0003_alter_profile_image"),
        ("posts", "0002_alter_post_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="user",
        ),
        migrations.AddField(
            model_name="post",
            name="user_profile",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="post",
                to="profiles.profile",
            ),
        ),
    ]
