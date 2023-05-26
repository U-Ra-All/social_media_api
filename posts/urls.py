from django.urls import path, include
from rest_framework import routers

from posts.views import (
    PostViewSet,
    CreatePostViewSet,
    MyPostViewSet,
)

router = routers.DefaultRouter()
router.register("", PostViewSet)

urlpatterns = [
    path("me/", MyPostViewSet.as_view()),
    path("create/", CreatePostViewSet.as_view()),
    path("", include(router.urls)),
]
app_name = "posts"
