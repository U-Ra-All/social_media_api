from django.urls import path, include
from rest_framework import routers

from profiles.views import ProfileViewSet, MyProfileViewSet

router = routers.DefaultRouter()
router.register("", ProfileViewSet)

urlpatterns = [
    path("me/", MyProfileViewSet.as_view()),
    path("", include(router.urls)),
]
app_name = "profiles"
