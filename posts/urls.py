from django.urls import path, include
from rest_framework import routers

from posts.views import (
    PostViewSet,
    CreatePostViewSet,
    MyPostsViewSet,
    FollowsPostsViewSet,
    LikeViewSet,
    CreateCommentViewSet,
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
        "like/",
        LikeViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    path("like/<int:pk>/", LikeViewSet.as_view({"post": "like"})),
    path("unlike/<int:pk>/", LikeViewSet.as_view({"post": "unlike"})),
    path("<int:pk>/comment", CreateCommentViewSet.as_view({"post": "create"})),
    path("", include(router.urls)),
]
app_name = "posts"
