from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from permissions import IsAdminOrIfAuthenticatedReadOnly
from posts.models import Post, Like, Comment
from posts.serializers import PostSerializer, CommentSerializer
from posts.tasks import publish_post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        """Retrieve the posts with filters"""
        title = self.request.query_params.get("title")
        text = self.request.query_params.get("text")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if text:
            queryset = queryset.filter(body__icontains=text)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                type=OpenApiTypes.STR,
                description="Filter by title (ex. ?title=My first post)",
            ),
            OpenApiParameter(
                "text",
                type=OpenApiTypes.STR,
                description="Filter by text (ex. ?text=post part)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CreatePostViewSet(generics.CreateAPIView):
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)


class MyPostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Post.objects.filter(user_profile=self.request.user.profile)
        return queryset


class FollowsPostsViewSet(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Post.objects.filter(
            user_profile__in=request.user.profile.follows.all()
        )
        serializer = self.serializer_class(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class LikeViewSet(viewsets.ViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Post.objects.filter(
            likes__in=Like.objects.filter(user_profile=request.user.profile)
        )
        serializer = self.serializer_class(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def like(self, request, pk):
        own_profile = request.user.profile
        liked_post = get_object_or_404(Post, id=pk)

        like = Like(post=liked_post, user_profile=own_profile)
        like.save()
        own_profile.likes.add(like)

        return Response(
            {f"message": f"you like {liked_post.title} post"},
            status=status.HTTP_200_OK,
        )

    def unlike(self, request, pk):
        own_profile = request.user.profile
        liked_post = get_object_or_404(Post, id=pk)

        like = get_object_or_404(Like, post=liked_post, user_profile=own_profile)
        own_profile.likes.filter(id=like.id).delete()

        return Response(
            {f"message": f"you unlike {liked_post.title} post"},
            status=status.HTTP_200_OK,
        )


class CreateCommentViewSet(viewsets.ViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            body = serializer.data["body"]
            post = get_object_or_404(Post, pk=pk)
            user_profile = post.user_profile
            Comment.objects.create(
                body=body, post=post, user_profile=user_profile
            )

            return Response(status=status.HTTP_201_CREATED)


class CreatePostWithDelayViewSet(viewsets.ViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def create_with_delay(self, request, delay):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            post = Post(
                title=serializer.data.get("title"),
                body=serializer.data.get("body"),
                user_profile=self.request.user.profile,
            )
            publish_post(post, delay)

            return Response(status=status.HTTP_200_OK)
