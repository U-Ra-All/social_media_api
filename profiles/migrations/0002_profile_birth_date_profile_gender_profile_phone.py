# Generated by Django 4.2.1 on 2023-05-23 07:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="birth_date",
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="gender",
            field=models.PositiveSmallIntegerField(
                choices=[(1, "Male"), (2, "Female"), (3, "Other")], default=1
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="phone",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
