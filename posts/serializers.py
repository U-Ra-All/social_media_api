from rest_framework import serializers

from posts.models import Post, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source="post.title", read_only=True)
    user_full_name = serializers.CharField(
        source="user_profile.full_name", read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "created_at",
            "body",
            "post_title",
            "user_full_name",
        )


class LikeSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source="post.title", read_only=True)
    user_full_name = serializers.CharField(
        source="user_profile.full_name", read_only=True
    )

    class Meta:
        model = Like
        fields = (
            "id",
            "created_at",
            "post_title",
            "user_full_name",
        )


class PostSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(
        source="user_profile.full_name", read_only=True
    )
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = (
            "id",
            "created_at",
            "title",
            "body",
            "user_full_name",
            "comments",
            "likes",
            "image",
        )
