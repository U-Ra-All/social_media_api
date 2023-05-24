from rest_framework import serializers

from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "created_at",
            "user",
            "first_name",
            "last_name",
            "gender",
            "birth_date",
            "phone",
            "follows",
        )
