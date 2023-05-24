from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from profiles.models import Profile
from profiles.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.prefetch_related("follows")
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Retrieve the movies with filters"""
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        phone = self.request.query_params.get("phone")

        queryset = self.queryset

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        if phone:
            queryset = queryset.filter(phone__icontains=phone)

        return queryset.distinct()
