from django.urls import path, include
from rest_framework import routers

from profiles.views import (
    ProfileViewSet,
    CreateProfileViewSet,
    MyProfileViewSet,
    FollowViewSet,
)

router = routers.DefaultRouter()
router.register("", ProfileViewSet)

urlpatterns = [
    path("me/", MyProfileViewSet.as_view()),
    path("create/", CreateProfileViewSet.as_view()),
    path("follow/", FollowViewSet.as_view({"get": "list"})),
    path("follow/<int:pk>/", FollowViewSet.as_view({"post": "follow"})),
    path("unfollow/<int:pk>/", FollowViewSet.as_view({"post": "unfollow"})),
    path("", include(router.urls)),
]
app_name = "profiles"
