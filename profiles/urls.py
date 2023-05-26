from django.urls import path, include
from rest_framework import routers

from profiles.views import ProfileViewSet, MyProfileViewSet, FollowViewSet

router = routers.DefaultRouter()
router.register("", ProfileViewSet)

urlpatterns = [
    path("me/", MyProfileViewSet.as_view()),
    path("follow/<int:pk>/", FollowViewSet.as_view({"post": "follow"})),
    path("unfollow/<int:pk>/", FollowViewSet.as_view({"post": "unfollow"})),
    path("", include(router.urls)),
]
app_name = "profiles"
