from rest_framework import generics, viewsets
from rest_framework.response import Response

from permissions import IsAdminOrIfAuthenticatedReadOnly
from posts.models import Post
from posts.serializers import PostSerializer
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
