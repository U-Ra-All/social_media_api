from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(
        source="user.profile.full_name", read_only=True
    )
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = (
            "id",
            "created_at",
            "title",
            "body",
            "user_full_name",
            "image",
        )
