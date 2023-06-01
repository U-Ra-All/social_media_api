from django.urls import path, include
from rest_framework import routers

from posts.views import (
    PostViewSet,
    CreatePostViewSet,
    MyPostsViewSet,
    FollowsPostsViewSet,
    LikedPostsViewSet,
    CreateCommentViewSet,
    CreatePostWithDelayViewSet,
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
        FollowsPostsViewSet.as_view(),
    ),
    path("create/", CreatePostViewSet.as_view()),
    path("liked/", LikedPostsViewSet.as_view({"get": "list"})),
    path("like/<int:pk>/", LikedPostsViewSet.as_view({"post": "like"})),
    path("unlike/<int:pk>/", LikedPostsViewSet.as_view({"post": "unlike"})),
    path("<int:pk>/comment", CreateCommentViewSet.as_view()),
    path(
        "create-with-delay/<int:delay>/",
        CreatePostWithDelayViewSet.as_view(),
    ),
    path("", include(router.urls)),
]
app_name = "posts"
