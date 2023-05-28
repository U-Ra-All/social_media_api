from django.urls import path, include
from rest_framework import routers

from posts.views import (
    PostViewSet,
    CreatePostViewSet,
    MyPostsViewSet,
    FollowsPostsViewSet,
    LikedPostsViewSet,
)

router = routers.DefaultRouter()
router.register("", PostViewSet)

urlpatterns = [
    path(
        "me/",
        MyPostsViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    path(
        "me/<int:pk>/",
        MyPostsViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "me/follows-posts/",
        FollowsPostsViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    path("create/", CreatePostViewSet.as_view()),
    path(
        "me/liked/",
        LikedPostsViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    path("", include(router.urls)),
]
app_name = "posts"
