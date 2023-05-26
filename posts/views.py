from rest_framework import generics, viewsets

from permissions import IsAdminOrIfAuthenticatedReadOnly
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class CreatePostViewSet(generics.CreateAPIView):
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyPostViewSet(
    generics.RetrieveUpdateDestroyAPIView,
):
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.post
