from rest_framework import routers

from profiles.views import ProfileViewSet

router = routers.DefaultRouter()
router.register("", ProfileViewSet)

urlpatterns = router.urls

app_name = "profiles"
