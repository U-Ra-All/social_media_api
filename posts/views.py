from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.response import Response

from permissions import IsAdminOrIfAuthenticatedReadOnly
from posts.models import Post, Like, Comment
from posts.serializers import PostSerializer, LikeSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser


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


class FollowsPostsViewSet(viewsets.ViewSet):
    queryset = Post.objects.all()

    def list(self, request):
        queryset = Post.objects.filter(
            user_profile__in=request.user.profile.follows.all()
        )
        serializer = PostSerializer(queryset, many=True)

        return Response(serializer.data)


class LikeViewSet(viewsets.ViewSet):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Post.objects.filter(
            likes__in=Like.objects.filter(user_profile=request.user.profile)
        )
        serializer = PostSerializer(queryset, many=True)

        return Response(serializer.data)

    def like(self, request, pk):
        own_profile = request.user.profile
        liked_post = Post.objects.get(id=pk)

        like = Like(post=liked_post, user_profile=own_profile)
        like.save()
        own_profile.likes.add(like)

        return Response(
            {f"message": f"you like {liked_post.title} post"},
            status=status.HTTP_200_OK,
        )

    def unlike(self, request, pk):
        own_profile = request.user.profile
        liked_post = Post.objects.get(id=pk)

        like = Like.objects.get(post=liked_post, user_profile=own_profile)
        own_profile.likes.filter(id=like.id).delete()

        return Response(
            {f"message": f"you unlike {liked_post.title} post"},
            status=status.HTTP_200_OK,
        )


class CreateCommentViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, pk):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            body = serializer.data["body"]
            post = get_object_or_404(Post, pk=pk)
            user_profile = post.user_profile
            Comment.objects.create(
                body=body, post=post, user_profile=user_profile
            )

            return Response(status=status.HTTP_201_CREATED)
